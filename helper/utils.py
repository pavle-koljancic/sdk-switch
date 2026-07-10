import json
import os
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from exceptions.exceptions import NSOError
from exceptions.exceptions import OfMissingEnvironmentVariablesError
from models.config.nso_config import NSOConfig
from models.nso.nso_base_result import NsoBaseResult
from models.nso.nso_query_strategy import NsoBaseParameters
from models.nso.nso_query_strategy import NsoQueryStrategy
from task_logging.task_logger import get_task_logger

task_logger = get_task_logger()


def execute_nso_restconf_query_request(nso_config: NSOConfig, request_body: str) -> requests.Response:
    """Execute POST request to '/restconf/tailf/query' endpoint (RESTCONF Query API)

    Args:
        nso_config (NSOConfig): Cisco NSO configuration.
        request_body (str): POST request body.

    Returns:
        Response: Response object.
    """
    headers = {"Content-Type": "application/yang-data+json"}
    url = f"http://{nso_config.nso_host}:{nso_config.nso_port}/restconf/tailf/query"

    task_logger.info("Performing POST request to %s", url)
    try:
        return requests.post(
            url=url,
            auth=HTTPBasicAuth(nso_config.nso_user, nso_config.nso_password),
            json=json.loads(request_body),
            headers=headers,
        )
    except Exception as e:
        error_message = (
            f"Failed to execute POST request to the NSO at '{url}'. "
            f"This could be due to network issues, incorrect URL, or the NSO service being unavailable. "
            f"Error details: {e}. Please check network connectivity, and try again."
        )
        raise NSOError(error_message) from e


def fetch_query_results(strategy: NsoQueryStrategy, parameters: NsoBaseParameters) -> list[NsoBaseResult]:
    body = strategy.build_body(parameters, strategy.result_model.selects())
    request_body = json.dumps(body)

    nso_config = NSOConfig()

    task_logger.info("Executing NSO query %s:  body=%s", strategy.name, request_body)

    response = execute_nso_restconf_query_request(nso_config, request_body)
    task_logger.info("NSO query %s response code: %s", strategy.name, response.status_code)
    task_logger.info("NSO query %s response body: %s", strategy.name, response.text)

    response_data: dict[str, Any] = response.json()
    return strategy.parse_response(response_data)


def get_executed_sql_query(query: str, params: list[Any]) -> str:
    if len(params) == 1 and isinstance(params[0], list):
        array_str = "ARRAY[" + ",".join(f"'{x}'" for x in params[0]) + "]"
        return query % array_str
    return query % tuple(repr(p) for p in params)


def check_env_vars(required_env_vars: list[str]) -> None:
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        raise OfMissingEnvironmentVariablesError(missing_vars)


def check_svlan_int_to_str(svlan: Any) -> Any | str:
    return str(svlan) if isinstance(svlan, int) and svlan >= 0 else svlan


def resolve_host_path(container_path: str | None) -> str:
    """
    Convert a container file path to its corresponding host path based on known volume mounts.
    """
    path_mappings = {
        "/home/app/files/huawei": "/home/frinx/huawei",
        "/home/app/files/siae": "/home/frinx/siae",
    }

    if container_path is None:
        return ""

    for mount_path, host_path in path_mappings.items():
        if container_path.startswith(mount_path):
            return container_path.replace(mount_path, host_path, 1)

    # No mapping found; return the original container path
    return container_path
