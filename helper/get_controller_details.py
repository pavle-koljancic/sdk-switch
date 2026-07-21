from typing import TypeVar

import requests

from pydantic import BaseModel
from requests.auth import HTTPBasicAuth

from exceptions.exceptions import NSOError
from models.config.nso_config import NSOConfig
from task_logging.task_logger import get_task_logger

T = TypeVar("T", bound=BaseModel)

task_logger = get_task_logger()

def get_controller_details(controller_type: str, model_class: type[T]) -> T:
    headers = {"Accept": "application/yang-data+json"}

    nso_config = NSOConfig()
    base_url = f"http://{nso_config.nso_host}:{nso_config.nso_port}/restconf/data"
    url = f"{base_url}/{controller_type}"

    task_logger.info("Performing GET request to %s", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(nso_config.nso_user, nso_config.nso_password),
        )
        response.raise_for_status()
        task_logger.info("Response code %s", response.status_code)

    except requests.exceptions.RequestException as e:
        raise NSOError(f"Problem when executing GET request to NSO at {url} - {e}") from e

    return model_class.model_validate(response.json().get(controller_type))
