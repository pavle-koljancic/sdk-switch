from datetime import UTC
from datetime import datetime
from typing import Any
from typing import cast
from zoneinfo import ZoneInfo

import requests
from conductor.client.configuration.configuration import Configuration

from task_logging.task_logger import get_task_logger

task_logger = get_task_logger()

config = Configuration()


def get_workflow_data(workflow_id: str) -> dict[str, Any]:
    """Fetches workflow details by workflow ID from Conductor API as a dictionary."""
    url = f"{config.host}/workflow/{workflow_id}"

    try:
        response = requests.get(url, headers={})
        response.raise_for_status()
        return cast(dict[str, Any], response.json())
    except requests.RequestException as e:
        task_logger.error(f"Error fetching workflow {workflow_id}: {e}")
        raise e


def generate_timestamp(ms_timestamp: int | None) -> str:
    """Returns a CET timestamp string from a millisecond UNIX timestamp or current time."""
    if ms_timestamp:
        dt_utc = datetime.fromtimestamp(ms_timestamp / 1000, tz=UTC)
    else:
        dt_utc = datetime.now(UTC)

    cet = dt_utc.astimezone(ZoneInfo("Europe/Bratislava"))
    return cet.strftime("%Y%m%d-%H%M%S-%Z")
