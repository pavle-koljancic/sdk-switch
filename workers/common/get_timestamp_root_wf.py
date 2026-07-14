from typing import Any

from conductor.client import worker_task
from conductor.client.http.models.task_def import TaskDef

from helper.timestamp_utils import generate_timestamp
from helper.timestamp_utils import get_workflow_data
from task_logging.task_logger import get_task_logger

task_logger = get_task_logger()


@worker_task(
    task_definition_name="get_timestamp_of_root_wf",
    register_task_def=True,  # Auto-register on startup
    task_def=TaskDef(
        description="Gets the timestamp of root workflow", timeout_seconds=180, response_timeout_seconds=180
    ),
)
def get_timestamp_root_wf(workflow_id: str) -> str:
    workflow_data: dict[str, Any] = get_workflow_data(workflow_id)

    while workflow_data and workflow_data.get("parentWorkflowId"):
        parent_id = workflow_data["parentWorkflowId"]
        task_logger.info(f"Parent workflow ID: {parent_id}")
        workflow_data = get_workflow_data(parent_id)

    timestamp = generate_timestamp(workflow_data.get("createTime", None))

    if timestamp is None:
        raise ValueError("Timestamp of root workflow is not found!")

    return timestamp
