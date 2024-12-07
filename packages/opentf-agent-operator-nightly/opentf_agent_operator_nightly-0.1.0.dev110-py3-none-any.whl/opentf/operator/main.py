# Copyright (c) 2024 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Create agents for a Kube orchestrator."""

from typing import Any, Dict, List, Optional, Set, Tuple, Union

import base64
import concurrent.futures
import hashlib
import json
import logging
import os
import random
import string
import threading
import time

from collections import defaultdict
from queue import Queue, Empty

import kopf
import requests

from kubernetes import client, config, stream

########################################################################
### Exceptions


class OperatorException(Exception):
    """OperatorException class"""

    def __init__(self, msg, details=None):
        self.msg = msg
        self.details = details


class NotFound(OperatorException):
    """AgentNotFound exception."""


class PodError(OperatorException):
    """PodError exception."""


class ThreadError(OperatorException):
    """ThreadError exception."""


class AgentError(OperatorException):
    """ThreadError exception."""


########################################################################
### Loggers


class ContextFilter(logging.Filter):
    def __init__(self, namespace, name) -> None:
        super().__init__()
        self.namespace = namespace
        self.name = name

    def filter(self, record):
        record.name = record.name.partition('_')[0]
        record.context = f'{self.namespace}/{self.name}'
        return True


def setup_logger(logger_name: str, name: str, namespace: str):
    logger = logging.getLogger(f'{logger_name}_{name}-{namespace}')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.hasHandlers():
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)-20s [%(levelname)-8s] [%(context)s] %(message)s'
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if not any(isinstance(f, ContextFilter) for f in logger.filters):
        logger.addFilter(ContextFilter(namespace, name))
    return logger


########################################################################
### Constants

POOLS_API_GROUP = 'agent.opentestfactory.org'
POOLS_API_VERSION = 'v1alpha1'
POOLS_KIND = 'pools'
AGENT_VERSION = '1.9'
AGENT_LIVENESS_PROBE = 300
AGENTS_URL_TMPL = '{pod}/agents'
AGENT_ID_URL_TMPL = '{pod}/agents/{agent_id}'
FILE_URL_TMPL = '{agent_url}/files/{file_id}'


REGISTRATION = {
    'apiVersion': 'opentestfactory.org/v1alpha1',
    'kind': 'AgentRegistration',
    'metadata': {'name': 'test agent', 'namespaces': [], 'version': AGENT_VERSION},
    'spec': {
        'tags': [],
        'encoding': 'utf-8',
        'liveness_probe': AGENT_LIVENESS_PROBE,
    },
}

AGENTS_WITH_POD = defaultdict(dict)
CREATE_AGENTS_PATH = 'status.create_agents.agents'
AGENTS_PODS_PATH = 'status.create_agents.agents_pods'

REQUEST_TIMEOUT = 60
POD_TIMEOUT = 60
BUSY_AGENTS_POLLING_DELAY = 10
IDLE_AGENTS_POLLING_DELAY = 5
HANDLER_RECOVERY_DELAY = 60


MAX_WORKERS = 10


########################################################################
### Helpers


def _as_list(what: Union[str, List[str]]) -> List[str]:
    return [what] if isinstance(what, str) else what


def _get_path(src: Dict[str, Any], path: List[str], msg: Optional[str] = None) -> Any:
    if not path:
        return src
    try:
        return _get_path(src[path[0]], path[1:])
    except (KeyError, TypeError) as err:
        txt = msg or f"Failed to get custom resource property {'.'.join(path)}"
        raise KeyError(txt) from err


def _create_body(path: str, value: Any) -> Dict[str, Any]:
    keys = path.split('.')
    patch_body = value
    for key in reversed(keys):
        patch_body = {key: patch_body}
    return patch_body


def _load_config():
    """Load kube local config or cluster config depending on context."""
    if os.environ.get('OPERATOR_CONTEXT') == 'local':
        config.load_kube_config()
    else:
        config.load_incluster_config()


def _make_copy(what):
    return json.loads(json.dumps(what))


def _make_suffix(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def _make_resource_id(name: str, namespace: str) -> str:
    name_hash = hashlib.md5(name.encode()).hexdigest()[:10]
    return f'{name}-{namespace}-{name_hash}-{_make_suffix(length=5)}'


def _make_agent_name(pool_name: str, namespace: str) -> str:
    return f'{pool_name}-{namespace}-{_make_suffix(length=5)}'


def _patch_pools_live(name: str, namespace: str, body: Dict[str, Any]):
    """Patch pools object via API call."""
    _load_config()
    custom_object_api = client.CustomObjectsApi()
    custom_object_api.patch_namespaced_custom_object(
        group=POOLS_API_GROUP,
        version=POOLS_API_VERSION,
        namespace=namespace,
        plural=POOLS_KIND,
        name=name,
        body=body,
    )


def _get_live_status(name: str, namespace: str, logger) -> Dict[str, Any]:
    """Get pools object live status."""
    _load_config()
    custom_object_api = client.CustomObjectsApi()
    try:
        obj = custom_object_api.get_namespaced_custom_object(
            group=POOLS_API_GROUP,
            version=POOLS_API_VERSION,
            namespace=namespace,
            plural=POOLS_KIND,
            name=name,
        )
        return obj.get('status', {})  # type: ignore
    except Exception as err:
        logger.error(f'Error fetching live status: {err}.')
        return {}


def _get_param_or_fail(
    source: Dict[str, Any], path: List[str], msg: Optional[str] = None
) -> Any:
    try:
        return _get_path(source, path, msg)
    except KeyError as err:
        raise kopf.TemporaryError(str(err))


def _make_headers(
    spec: Dict[str, Any], namespace: str, logger
) -> Optional[Dict[str, str]]:
    token = None
    if secret_name := spec.get('orchestratorSecret'):
        _load_config()
        core_api = client.CoreV1Api()
        try:
            secret = core_api.read_namespaced_secret(secret_name, namespace)
            token = base64.b64decode(secret.data['token']).decode('utf-8')  # type: ignore
        except Exception as err:
            logger.error(str(err))
    return {'Authorization': f'Bearer {token}'} if token else None


def _get_pod() -> str:
    if not (pod := os.environ.get('ORCHESTRATOR_URL')):
        raise NotFound('Cannot retrieve orchestrator url.')
    return pod


def _get_pod_url_and_headers(
    spec: Dict[str, Any], namespace: str, logger
) -> Tuple[str, Optional[Dict[str, str]]]:
    try:
        url = AGENTS_URL_TMPL.format(pod=_get_pod())
        headers = _make_headers(spec, namespace, logger)
        return url, headers
    except NotFound as err:
        raise ThreadError('Error in agents monitoring thread:', err) from err


########################################################################
### /agents requests handling


def _register_agent(
    agent_name: str,
    agent_namespaces,
    url: str,
    tags: Union[str, List[str]],
    headers: Optional[Dict[str, str]],
    logger,
) -> requests.Response:
    """Register agent on orchestrator.

    # Required arguments

    - agent_name: a string,
    - url: a string, agentchannel endpoint url,
    - tags: a string or list of strings, agent tags
    - headers: a dictionary or None, authorization headers
    - logger: a logger

    # Returned values

    - response: a request response

    # Raised exception

    AgentError exception when agent registration fails.
    """
    REGISTRATION['spec']['tags'] = _as_list(tags)
    REGISTRATION['metadata']['name'] = agent_name
    REGISTRATION['metadata']['namespaces'] = agent_namespaces
    logger.debug(
        f'Registering agent. Name: {agent_name}, tags: {REGISTRATION["spec"]["tags"]}.'
    )
    response = requests.post(
        url, json=REGISTRATION, headers=headers, timeout=REQUEST_TIMEOUT
    )

    if response.status_code != 201:
        raise AgentError(
            f'Failed to register agent: error code {response.status_code}, {response.text}'
        )
    logger.debug(response.json()['message'])
    return response


def _maybe_get_agent_command(
    agent_id: str, spec: Dict[str, Any], namespace: str, logger
) -> Optional[Dict[str, Any]]:
    """Try to get a command from agent.

    # Required arguments

    - agent_id: a string, agent uuid
    - spec: a dictionary, pool resource `spec` property content
    - namespace: a string, pool resource namespace
    - logger: a logger

    # Returned values

    None when agentchannel responds 204 and command when agentchannel
    responds 200.
    """
    pod, headers = _get_pod(), _make_headers(spec, namespace, logger)
    url = AGENT_ID_URL_TMPL.format(agent_id=agent_id, pod=pod)

    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    if response.status_code == 204:
        return None
    if response.status_code == 200 and 'details' in response.json():
        return response.json()['details']
    raise NotFound(f'Agent {agent_id} not found or .details not in response.')


def _deregister_agent(
    pod: str, agent_id: str, headers: Optional[Dict[str, str]], logger
) -> None:
    url = AGENT_ID_URL_TMPL.format(pod=pod, agent_id=agent_id)
    logger.info(f'De-registering agent {agent_id}.')
    response = requests.delete(url, headers=headers, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        raise AgentError(
            f'Cannot de-register agent {agent_id}: {response.json()["message"]}'
        )
    logger.debug(response.json()['message'])


def _deregister_agents(
    agents: List[str],
    resource_id: str,
    pod: str,
    headers: Optional[Dict[str, Any]],
    logger,
):
    """De-register agents.

    # Required arguments

    - agents: a list, agents uuids
    - resource_id: a string, pool resource id
    - pod: a string, orchestrator pod url
    - headers: a dictionary, authorization headers
    - logger: a logger

    # Returned values

    - agents: a list, remaining agents uuids
    - busy: a list, busy agents uuids
    """
    busy = []
    for agent_id in agents.copy():
        if agent_id not in AGENTS_WITH_POD.get(resource_id, {}):
            _deregister_agent(pod, agent_id, headers, logger)
            agents.remove(agent_id)
        else:
            busy.append(agent_id)
    return agents, busy


def _attempt_agent_removal(
    agents: List[str],
    resource_name: str,
    resource_id: str,
    namespace: str,
    pod: str,
    headers: Optional[Dict[str, Any]],
    logger,
):
    """Try to de-register agents. If some agents are busy, wait and retry."""
    while True:
        agents, busy = _deregister_agents(agents, resource_id, pod, headers, logger)
        with PENDING_AGENTS_LOCK:
            _patch_pools_live(
                resource_name,
                namespace,
                _create_body(
                    CREATE_AGENTS_PATH,
                    list(set(agents + busy)),
                ),
            )
        if not agents:
            break
        logger.info('Some agents still busy, they will be de-registered on release.')
        time.sleep(BUSY_AGENTS_POLLING_DELAY)


def _get_agents(
    url: str, name: str, namespace: str, headers: Optional[Dict[str, str]], logger
) -> List[Dict[str, Any]]:
    """Get agents from agentchannel.

    # Required arguments

    - url: a string, agentchannel url
    - name: a string, pool name
    - namespace: a string, pool namespace
    - headers: a dictionary or None, authorization headers
    - logger: a logger

    # Returned value

    A list of AgentRegistration manifests.
    """
    logger.debug(f'Retrieving registered agents from {url}.')
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        raise AgentError(
            f'Cannot retrieve registered agents list: {response.json()["message"]}'
        )
    if not response.json()['items']:
        logger.debug('No registered agent found.')
        return []
    logger.debug('Agents list retrieved.')
    return [
        item
        for item in response.json()['items']
        if item['metadata']['name'].startswith(f'{name}-{namespace}')
    ]


def _register_agents_return_uuids(
    pool_size: int, pool_name: str, spec: Dict[str, Any], namespace: str, logger
) -> List[str]:
    """Register n agents and return registered agents info.

    # Required arguments
      - pool_size: an integer, agents pool size
      - resource_name: a string, used to generate agent name
      - spec: a dictionary, pool specification
      - namespace: a string, namespace
      - logger: a logger instance

    # Returned values
      - agents: a list, agents uuids
      - version: a string, orchestrator version

    # Raised exceptions
    Raises an AgentError exception if agent registration fails.
    """
    tags, pod = _get_param_or_fail(spec, ['tags']), _get_pod()
    ns = spec.get('namespaces', '')
    if isinstance(ns, list):
        ns = ','.join(ns)
    headers = _make_headers(spec, namespace, logger)
    url = AGENTS_URL_TMPL.format(pod=pod)
    agents = []
    for _ in range(pool_size):
        agent_name = _make_agent_name(pool_name, namespace)
        response = _register_agent(
            agent_name,
            ns,
            url,
            tags,
            headers,
            logger,
        )
        if response.status_code != 201:
            raise AgentError(
                f'Failed to register agent {agent_name}: {response.json()["message"]}.'
            )
        details = response.json()['details']
        agents.append(details['uuid'])
    return agents


########################################################################
### Execution on pods

AGENTS_POLLING_DELAY = 5
POOLS_THREADS = {}
AGENTS_COMMANDS = {}
ACTIVE_AGENTS = {}


PENDING_AGENTS_LOCK = threading.Lock()


def _get_pod_template(pod_name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    template = _make_copy(
        _get_param_or_fail(
            spec, ['template'], 'Failed to get pod template from pools definition'
        )
    )
    template['api_version'] = 'v1'
    template['kind'] = 'Pod'
    template.setdefault('metadata', {})['name'] = pod_name
    return template


def _create_exec_pod(
    pod_name: str, namespace: str, spec: Dict[str, Any], api_instance, logger
):
    """Create a pod for an agent. Raise exception if creation fails."""
    pod_template = _get_pod_template(pod_name, spec)
    existing_pods = api_instance.list_namespaced_pod(namespace=namespace)

    if existing_pods and pod_name in [pod.metadata.name for pod in existing_pods.items]:
        logger.debug(
            f'Pod `{pod_name}` in namespace `{namespace}` already exists, will not create new one.'
        )
        return
    try:
        api_instance.create_namespaced_pod(namespace=namespace, body=pod_template)
        logger.info(f'Pod `{pod_name}` created in namespace `{namespace}`.')
    except Exception as err:
        raise PodError(
            f'Failed to create pod `{pod_name}` in namespace `{namespace}`: {str(err)}'
        ) from err


def _delete_exec_pod(pod_name: str, namespace: str, logger):
    """Delete a pod related to an inactive agent."""
    try:
        api_instance = client.CoreV1Api()
        api_instance.delete_namespaced_pod(name=pod_name, namespace=namespace)
        logger.info(f'Pod `{pod_name}` deleted from namespace `{namespace}`.')
    except Exception as err:
        logger.error(
            f'Cannot delete pod `{pod_name}` from namespace `{namespace}`: {str(err)}'
        )


def _is_pod_running(
    pod_name: str, namespace: str, api_instance: client.CoreV1Api
) -> bool:
    timeout = time.time() + POD_TIMEOUT
    while time.time() <= timeout:
        pod_status = api_instance.read_namespaced_pod_status(
            pod_name, namespace=namespace
        )
        if pod_status.status.phase == 'Running':  # type: ignore
            return True
        time.sleep(1)
    return False


def _read_pod_response(pod_response) -> Tuple[str, str, int]:
    stdout, stderr = '', ''
    while pod_response.is_open():
        pod_response.update(timeout=1)
        if pod_response.peek_stdout():
            stdout += pod_response.read_stdout()
        if pod_response.peek_stderr():
            stderr += pod_response.read_stderr()
    return_code = pod_response.returncode
    pod_response.close()
    return stdout, stderr, return_code


def _upload_file_to_pod(
    agent_url: str,
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    namespace: str,
    command: Dict[str, Any],
    api_instance,
):
    kind = command['kind']
    path = command['path'] if kind == 'put' else command['filename']
    cmd = ['/bin/sh', '-c', f'cat > {path}']
    pod_response = stream.stream(
        api_instance.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
        command=cmd,
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
        _preload_content=False,
    )
    if kind == 'put':
        response = requests.get(
            agent_url, stream=True, headers=headers, timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise Exception(
                f'Failed to get filestream from orchestrator, error code: {response.status_code}.'
            )
        for chunk in response.iter_content(chunk_size=128):
            if not chunk:
                continue
            pod_response.write_stdin(chunk.decode('utf-8'))
    else:
        pod_response.write_stdin(command['content'])
    pod_response.close()


def _execute_cmd_on_pod(
    instruction: str, pod_name: str, namespace: str, api_instance: client.CoreV1Api
) -> Tuple[str, str, int]:
    cmd = ['/bin/sh', '-c', instruction]
    pod_response = stream.stream(
        api_instance.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
        command=cmd,
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
        _preload_content=False,
    )
    return _read_pod_response(pod_response)


def _process_put_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    namespace: str,
    api_instance: client.CoreV1Api,
    logger,
):
    """Download file from orchestrator to the agent pod."""
    if 'path' not in command:
        logger.error('No path specified in command.')
    if 'file_id' not in command:
        logger.error('No file_id specified in command.')
    url = FILE_URL_TMPL.format(agent_url=agent_url, file_id=command['file_id'])
    try:
        # TODO: what to do with working_dir / script_path ?
        if _is_pod_running(pod_name, namespace, api_instance):
            _upload_file_to_pod(
                url, headers, pod_name, namespace, command, api_instance
            )
        else:
            raise TimeoutError('Timed out, pod still not running')
    except Exception as err:
        result = requests.post(
            url,
            json={
                'details': {
                    'error': f'Failed to download file {command["file_id"]} to {command["path"]}: {err}'
                }
            },
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        logger.error(f'An error occurred while downloading file: {err}.')
        if result.status_code != 200:
            logger.debug(
                f'Failed to notify the orchestrator. Got a {result.status_code} status code.'
            )


def _process_exec_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    namespace: str,
    api_instance,
    logger,
):
    """Execute the execute command on a pod."""
    try:
        instruction = command['command']
        if _is_pod_running(pod_name, namespace, api_instance):
            stdout, stderr, return_code = _execute_cmd_on_pod(
                instruction, pod_name, namespace, api_instance
            )
        else:
            raise TimeoutError('Timed out, pod still not running')
        sent = False
        while not sent:
            try:
                result = requests.post(
                    agent_url,
                    json={
                        'stdout': stdout.splitlines(),
                        'stderr': stderr.splitlines(),
                        'exit_status': return_code,
                    },
                    headers=headers,
                    timeout=REQUEST_TIMEOUT,
                )
                sent = True
                if result.status_code != 200:
                    logger.error(
                        f'Failed to push command result. Response code {result.status_code}.'
                    )
            except Exception as err:
                logger.error(f'Failed to push command result: {str(err)}, retrying.')
    except Exception as err:
        logger.error(f'Failed to execute command: {str(err)}.')


def _process_get_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    namespace: str,
    api_instance,
    logger,
):
    """Upload file from the pod to the orchestrator."""
    if 'path' not in command:
        logger.error('No path specified in command.')
        return
    if 'file_id' not in command:
        logger.error('No file_id specified in command.')
        return
    url = FILE_URL_TMPL.format(agent_url=agent_url, file_id=command['file_id'])
    try:
        if _is_pod_running(pod_name, namespace, api_instance):
            file_base64, stderr, return_code = _execute_cmd_on_pod(
                f'base64 {command["path"]}', pod_name, namespace, api_instance
            )
            if return_code != 0:
                raise PodError(stderr)
            file_binary = base64.b64decode(file_base64)
            requests.post(
                url, data=file_binary, headers=headers, timeout=REQUEST_TIMEOUT
            )
        else:
            raise TimeoutError('Timed out, pod still not running.')
    except Exception as err:
        file_path = command['path']
        result = requests.post(
            agent_url,
            json={'details': {'error': f'Failed to fetch file {file_path}: {err}.'}},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        if result.status_code != 200:
            logger.error(
                f'Failed to push command result. Status code: {result.status_code}'
            )


def _process_run_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    namespace: str,
    api_instance,
    logger,
):
    """Upload script to pod as file, then execute the command."""
    try:
        if _is_pod_running(pod_name, namespace, api_instance):
            _upload_file_to_pod('', headers, pod_name, namespace, command, api_instance)
        else:
            raise TimeoutError('Timed out, pod still not running.')
        _process_exec_cmd(
            agent_url, command, headers, pod_name, namespace, api_instance, logger
        )
    except Exception as err:
        logger.error(f'Failed to run command: {str(err)}')


KIND_HANDLERS = {
    'put': _process_put_cmd,
    'exec': _process_exec_cmd,
    'get': _process_get_cmd,
    'run': _process_run_cmd,
}


def _kill_orphan_agent(
    pod: str,
    agent_id: str,
    headers: Optional[Dict[str, Any]],
    name: str,
    namespace: str,
    spec: Dict[str, Any],
    status: Dict[str, Any],
    logger,
):
    logger.debug('De-registering orphan agent, creating new agent instead.')
    with PENDING_AGENTS_LOCK:
        _deregister_agent(pod, agent_id, headers, logger)
        new_agent = _register_agents_return_uuids(1, name, spec, namespace, logger)
        agents_patch = [
            item for item in status['create_agents']['agents'] if item != agent_id
        ] + new_agent
        _patch_pools_live(
            name, namespace, _create_body(CREATE_AGENTS_PATH, agents_patch)
        )
        logger.debug(
            f'Agent {agent_id} de-registered, agent {new_agent[0]} created, status patched.'
        )


def _remove_agent_and_pod(
    agent_id: str,
    resource_id: str,
    resource_name: str,
    namespace: str,
    pod_name: str,
    logger,
):
    try:
        del AGENTS_WITH_POD[resource_id][agent_id]
        status = _get_live_status(resource_name, namespace, logger)
        if not AGENTS_WITH_POD[resource_id]:
            agents_pods = None
        elif agents_pods := status['create_agents'].get('agents_pods', None):
            agents_pods[agent_id] = None
        _patch_pools_live(
            resource_name, namespace, _create_body(AGENTS_PODS_PATH, agents_pods)
        )
    except KeyError:
        pass
    _delete_exec_pod(pod_name, namespace, logger)


def _refresh_idle_agents(
    pool: Set[str],
    url: str,
    headers: Optional[Dict[str, Any]],
    logger,
):
    agents = {agent: {} for agent in pool}
    try:
        response = requests.patch(
            url, json=agents, headers=headers, timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise AgentError(
                f'Failed to refresh idle agents: error code {response.status_code}, {response.text}'
            )
        logger.debug(f'Refreshed idle agents: {", ".join(pool)}')
    except Exception as err:
        logger.error('Error while touching agents: %s.', str(err))


def _cleanup_and_register_agents(
    name: str, namespace: str, resource_id: str, spec: Dict[str, Any], logger
):
    logger.warn(
        'No registered agent found. The orchestrator may have been down. Proceeding with cleanup and re-registering agents.'
    )
    if agents_pods := AGENTS_WITH_POD[resource_id]:
        with PENDING_AGENTS_LOCK:
            logger.debug('Cleaning up pods.')
            for data in agents_pods.values():
                _delete_exec_pod(data['pod'], namespace, logger)
            del AGENTS_WITH_POD[resource_id]
            _patch_pools_live(name, namespace, _create_body(AGENTS_PODS_PATH, None))
    to_create = spec.get('poolSize', 0)
    agents = _register_agents_return_uuids(to_create, name, spec, namespace, logger)
    _patch_pools_live(name, namespace, _create_body(CREATE_AGENTS_PATH, agents))
    logger.info(f'Recreated {to_create} agents.')


########################################################################
### Two little threads


def dispatch(
    agent_id: str,
    command: Dict[str, Any],
    name: str,
    namespace: str,
    spec: Dict[str, Any],
    logger,
):
    _load_config()
    api_instance = client.CoreV1Api()
    pod, headers = _get_pod(), _make_headers(spec, namespace, logger)
    try:
        pod_name = f"{spec.get('template', {}).get('metadata', {}).get('name', name)}-{agent_id}"
        status = _get_live_status(name, namespace, logger)
        resource_id = _get_param_or_fail(
            status,
            ['create_agents', 'resource_id'],
            'Cannot retrieve resource id, aborting.',
        )
        url = AGENT_ID_URL_TMPL.format(agent_id=agent_id, pod=pod)

        if command['kind'] in ('exec', 'run') and ('-2.sh' in command['command']):
            KIND_HANDLERS[command['kind']](
                url, command, headers, pod_name, namespace, api_instance, logger
            )
            time.sleep(0.5)
            if not _maybe_get_agent_command(agent_id, spec, namespace, logger):
                with PENDING_AGENTS_LOCK:
                    _remove_agent_and_pod(
                        agent_id,
                        resource_id,
                        name,
                        namespace,
                        pod_name,
                        logger,
                    )
                return
        if agent_id not in AGENTS_WITH_POD.get(resource_id, {}):
            try:
                _create_exec_pod(pod_name, namespace, spec, api_instance, logger)
                _patch_pools_live(
                    name,
                    namespace,
                    _create_body(AGENTS_PODS_PATH, {agent_id: pod_name}),
                )
                AGENTS_WITH_POD[resource_id][agent_id] = {
                    'command': True,
                    'pod': pod_name,
                }
            except PodError as err:
                logger.error(str(err))
                _kill_orphan_agent(
                    pod, agent_id, headers, name, namespace, spec, status, logger
                )
                return
        KIND_HANDLERS[command['kind']](
            url, command, headers, pod_name, namespace, api_instance, logger
        )
        with PENDING_AGENTS_LOCK:
            if AGENTS_WITH_POD.get(resource_id, {}).get(agent_id):
                AGENTS_WITH_POD[resource_id][agent_id]['command'] = False
            else:
                logger.info(
                    'Cannot set command state for agent %s, agent may have been cleaned up.',
                    agent_id,
                )
    except Exception as err:
        logger.error(
            'Error while handling agent commands: %s.',
            str(err),
        )


def handle_agent_command(
    stop_event: threading.Event, name: str, namespace: str, queue, max_workers: int
):
    """Agent commands handling thread.

    Waits for a command, creates an execution environment if required and processes
    a command. When channel release command (-2.sh) is received, deletes the execution
    environment.
    """
    logger = setup_logger('handle-commands', name, namespace)
    logger.info(
        'Starting agents commands handling thread.',
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while not stop_event.is_set():
            try:
                command = queue[f'{name}.{namespace}'].get(timeout=1)
                executor.submit(dispatch, *command)
            except Empty:
                continue
            except Exception as err:
                logger.error(
                    'Error in agents commands handling thread: %s.',
                    str(err),
                )
    logger.info('Stopping agents commands handling thread.')


def handle_active_agents(
    stop_event: threading.Event, name: str, namespace: str, spec: Dict[str, Any]
):
    logger = setup_logger('handle-agents', name, namespace)
    logger.info(
        'Starting active agents handling thread.',
    )
    name_ns = f'{name}.{namespace}'
    while not stop_event.is_set():
        try:
            agent, resource_id = ACTIVE_AGENTS[name_ns].get(timeout=1)
            already_active = AGENTS_WITH_POD.get(resource_id, {}).get(agent)
            if already_active and already_active.get('command'):
                continue
            if command := _maybe_get_agent_command(agent, spec, namespace, logger):
                AGENTS_COMMANDS[name_ns].put(
                    (agent, command, name, namespace, spec, logger)
                )
                if already_active:
                    AGENTS_WITH_POD[resource_id][agent]['command'] = True
        except Empty:
            continue
        except Exception as err:
            logger.error(
                'Error in active agents handling thread: %s',
                str(err),
            )
    logger.info(
        'Stopping active agents handling thread.',
    )


def monitor_agents(
    stop_event: threading.Event, name: str, namespace: str, spec: Dict[str, Any]
):
    logger = setup_logger('monitor-agents', name, namespace)
    logger.info(
        'Starting agents monitoring thread.',
    )
    url, headers = _get_pod_url_and_headers(spec, namespace, logger)

    while not stop_event.is_set():
        try:
            time.sleep(IDLE_AGENTS_POLLING_DELAY)
            status = _get_live_status(name, namespace, logger)
            kube_agents = status.get('create_agents', {}).get('agents', [])
            resource_id = status.get('create_agents', {}).get('resource_id')
            if not kube_agents:
                logger.debug('No agents found for resource. Will retry.')
                continue
            agents = _get_agents(url, name, namespace, headers, logger)
            active_agents = {
                agent['metadata']['agent_id']
                for agent in agents
                if agent['status']['phase'] == 'BUSY'
            }.intersection(kube_agents)
            idle_agents = {
                agent['metadata']['agent_id']
                for agent in agents
                if agent['status']['phase'] != 'BUSY'
            }.intersection(kube_agents)
            if not active_agents and not idle_agents:
                _cleanup_and_register_agents(name, namespace, resource_id, spec, logger)
                continue
            if idle_agents:
                _refresh_idle_agents(idle_agents, url, headers, logger)
            for agent in active_agents:
                ACTIVE_AGENTS[f'{name}.{namespace}'].put((agent, resource_id))
        except Exception as err:
            logger.error('Error while monitoring agents: %s.', str(err))
    logger.info(
        'Stopping agents monitoring thread.',
    )


def _stop_threads(resource_name: str):
    """Stop agents handling threads.

    # Required argument

    - resource_name: a string, `resource_name.namespace`

    # Raised exception

    ThreadError exception
    """
    if resource_name in POOLS_THREADS:
        threads_events = POOLS_THREADS.pop(resource_name)
        threads_events['monitor_stop_event'].set()
        threads_events['handle_stop_event'].set()
        threads_events['active_stop_event'].set()
        threads_events['monitor_thread'].join()
        threads_events['handle_thread'].join()
        threads_events['active_thread'].join()
        return
    raise ThreadError(f'No thread found for {resource_name}.')


def _start_threads(name: str, namespace: str, spec: Dict[str, Any]):
    """Start agents handling threads.

    # Required arguments

    - name: a string, pools resource name
    - namespace: a string, pools resource namespace
    - spec: a dictionary, pools resource definition `spec` property
    - version: a string, orchestrator version

    # Raised exception

    ThreadError exception.
    """
    try:
        name_ns = f'{name}.{namespace}'

        monitor_stop_event = threading.Event()
        active_stop_event = threading.Event()
        handle_stop_event = threading.Event()

        monitor_thread = threading.Thread(
            target=monitor_agents, args=(monitor_stop_event, name, namespace, spec)
        )
        monitor_thread.start()

        ACTIVE_AGENTS.setdefault(name_ns, Queue())
        active_thread = threading.Thread(
            target=handle_active_agents,
            args=(active_stop_event, name, namespace, spec),
        )
        active_thread.start()

        AGENTS_COMMANDS.setdefault(name_ns, Queue())
        handle_thread = threading.Thread(
            target=handle_agent_command,
            args=(handle_stop_event, name, namespace, AGENTS_COMMANDS, MAX_WORKERS),
        )
        handle_thread.start()

        POOLS_THREADS[name_ns] = {
            'monitor_thread': monitor_thread,
            'monitor_stop_event': monitor_stop_event,
            'active_thread': active_thread,
            'active_stop_event': active_stop_event,
            'handle_thread': handle_thread,
            'handle_stop_event': handle_stop_event,
        }
    except Exception as err:
        raise ThreadError('Failed to start threads: ', err) from err


########################################################################
### Kopf event handlers


@kopf.on.create(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND)  # type: ignore
def create_agents(spec, name, namespace, logger, **kwargs):
    """Register poolSize agents on orchestrator on pools resource creation
    and start agents handling threads."""
    try:
        pool_size = spec.get('poolSize', 0)
        if not isinstance(pool_size, int) or pool_size < 0:
            raise ValueError(f'Pool size must be a positive integer, got {pool_size}.')
        agents = _register_agents_return_uuids(pool_size, name, spec, namespace, logger)
        _start_threads(name, namespace, spec)
        return {
            'agents': agents,
            'resource_id': _make_resource_id(name, namespace),
        }
    except Exception as err:
        raise kopf.TemporaryError(
            f'Failed to register agents for pool {name} in namespace {namespace}: {err}. Handler will recover in a minute.',
            delay=HANDLER_RECOVERY_DELAY,
        )


@kopf.on.delete(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND)  # type: ignore
def delete_agents(name, namespace, spec, status, logger, **kwargs):
    """De-register agents on pools resource deletion and stop agents handling
    threads."""
    try:
        agents, pod = status.get('create_agents', {}).get('agents', []), _get_pod()
        headers = _make_headers(spec, namespace, logger)
        resource_id = _get_param_or_fail(
            status,
            ['create_agents', 'resource_id'],
            'Failed to get resource id, aborting.',
        )

        _attempt_agent_removal(
            agents, name, resource_id, namespace, pod, headers, logger
        )
        if AGENTS_WITH_POD.get(resource_id):
            del AGENTS_WITH_POD[resource_id]
        _stop_threads(f'{name}.{namespace}')
    except Exception as err:
        raise kopf.TemporaryError(
            f'Failed to delete agents for pool {name} in namespace {namespace}: {err}. Handler will recover in a minute.',
            delay=HANDLER_RECOVERY_DELAY,
        )


@kopf.on.resume(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND)  # type: ignore
def relaunch_agents(spec, status, name, namespace, logger, patch, **kwargs):
    """Check orchestrator agents state when resuming operator, harmonize
    it with pools resource spec, and start agents handling threads."""
    try:
        _load_config()
        pod, headers = _get_pod(), _make_headers(spec, namespace, logger)
        otf_agents_list = _get_agents(
            AGENTS_URL_TMPL.format(pod=pod),
            name,
            namespace,
            headers,
            logger,
        )
        otf_agents = [item['metadata']['agent_id'] for item in otf_agents_list]
        otf_busy_agents = [
            item['metadata']['agent_id']
            for item in otf_agents_list
            if (
                item['status'].get('phase') == 'BUSY'
                or item['status'].get('currentJobID')
            )
        ]
        kube_agents = status.get('create_agents', {}).get('agents', [])
        kube_agents_pods = status.get('create_agents', {}).get('agents_pods', {})
        for agent in otf_busy_agents:
            _deregister_agent(pod, agent, headers, logger)
            otf_agents.remove(agent)
            if agent in kube_agents_pods:
                _delete_exec_pod(kube_agents_pods[agent], namespace, logger)
        _patch_pools_live(name, namespace, _create_body(AGENTS_PODS_PATH, None))
        if not kube_agents:
            logger.debug('No agents found for this resource, will create some.')
            return create_agents(spec, name, namespace, logger)  # type: ignore
        if len(kube_agents) > len(otf_agents):
            to_create = len(kube_agents) - len(otf_agents)
            logger.debug(f'Recreating {to_create} agents.')
            agents = _register_agents_return_uuids(
                to_create, name, spec, namespace, logger
            )
            new_agents = list(set(kube_agents).intersection(set(otf_agents))) + agents
            patch.status['create_agents'] = {'agents': new_agents}
        _start_threads(name, namespace, spec)
    except Exception as err:
        raise kopf.TemporaryError(
            f'Failed to resume agents for pool {name} in namespace {namespace}: {err}. Handler will recover in a minute.',
            delay=HANDLER_RECOVERY_DELAY,
        )


@kopf.on.cleanup()  # type: ignore
def cleanup_threads(**kwargs):
    try:
        for name in POOLS_THREADS.copy():
            _stop_threads(name)
    except ThreadError as err:
        logger = logging.getLogger('cleanup')
        logger.error('Threads cleanup failed: %s.', str(err))


@kopf.on.field(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND, field='spec.poolSize')  # type: ignore
def update_pool_size(diff, spec, status, name, namespace, logger, patch, **kwargs):
    """Update orchestrator agents pool size when pools resource `spec.poolSize`
    value changes."""

    try:
        action, _, current_pool, new_pool = diff[0]
        if action == 'change' and (current_pool != new_pool):
            pod = _get_pod()
            current_agents = status.get('create_agents', {}).get('agents', [])
            resource_id = _get_param_or_fail(
                status,
                ['create_agents', 'resource_id'],
                'Failed to get resource id, aborting.',
            )
            if current_pool < new_pool:
                new_agents = _register_agents_return_uuids(
                    (new_pool - current_pool), name, spec, namespace, logger
                )
                patch.status['create_agents'] = {'agents': current_agents + new_agents}
            elif current_pool > new_pool:
                kill = current_pool - new_pool
                headers = _make_headers(spec, namespace, logger)
                idle_agents = set(current_agents) - set(AGENTS_WITH_POD[resource_id])
                if kill <= len(idle_agents):
                    morituri = list(idle_agents)[:kill]
                    for moriturus in morituri:
                        _deregister_agent(
                            pod,
                            moriturus,
                            headers,
                            logger,
                        )
                    with PENDING_AGENTS_LOCK:
                        _patch_pools_live(
                            name,
                            namespace,
                            _create_body(
                                CREATE_AGENTS_PATH,
                                list(set(current_agents) - set(morituri)),
                            ),
                        )
                else:
                    _attempt_agent_removal(
                        current_agents,
                        name,
                        resource_id,
                        namespace,
                        pod,
                        headers,
                        logger,
                    )
    except Exception as err:
        raise kopf.TemporaryError(
            f'Failed to update pool size for pool {name} in namespace {namespace}: {err}. Handler will recover in a minute.',
            delay=HANDLER_RECOVERY_DELAY,
        )


@kopf.on.field(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND, field='spec.tags')  # type: ignore
def update_tags(diff, spec, status, name, namespace, logger, **kwargs):
    """De-register current orchestrator agents pool and register new agents with
    updated tags when pools resource `spec.tags` value changes."""
    try:
        action, _, old_tags, new_tags = diff[0]
        if action == 'change' and (old_tags != new_tags):
            pod = _get_pod()
            if old_agents := status.get('create_agents', {}).get('agents'):
                headers = _make_headers(spec, namespace, logger)
                resource_id = _get_param_or_fail(
                    status,
                    ['create_agents', 'resource_id'],
                    'Failed to get resource id, aborting.',
                )
                new_agents = []
                while True:
                    old = len(old_agents)
                    old_agents, busy = _deregister_agents(
                        old_agents, resource_id, pod, headers, logger
                    )
                    add_agents = _register_agents_return_uuids(
                        (old - len(busy)), name, spec, namespace, logger
                    )
                    new_agents += add_agents
                    with PENDING_AGENTS_LOCK:
                        _patch_pools_live(
                            name,
                            namespace,
                            _create_body(
                                'status.create_agents',
                                {
                                    'agents': list(set(new_agents + busy)),
                                    'tags': new_tags,
                                },
                            ),
                        )
                    if not old_agents:
                        break
                    logger.info(
                        'Some agents still busy, tags will be updated on release.'
                    )
                    time.sleep(BUSY_AGENTS_POLLING_DELAY)
    except Exception as err:
        raise kopf.TemporaryError(
            f'Failed to update agents tags for pool {name} in namespace {namespace}: {err}. Handler will recover in a minute.',
            delay=HANDLER_RECOVERY_DELAY,
        )
