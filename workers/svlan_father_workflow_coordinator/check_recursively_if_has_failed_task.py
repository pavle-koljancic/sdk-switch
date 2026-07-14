from conductor.client import TaskResult
from conductor.client import TaskResultStatus
from conductor.client import worker_task
from conductor.client.http.models.task_def import TaskDef

from helper.wf_loader_v2 import build_workflow_data_tree


@worker_task(
    task_definition_name="check_recursively_if_has_failed_task",
    register_task_def=True,  # Auto-register on startup
    task_def=TaskDef(
        name="check_recursively_if_has_failed_task",  # Will be overridden by task_definition_name
        retry_count=0,
        timeout_seconds=180,
        response_timeout_seconds=180,
        description="Fetches all sub-workflows inside specified workflow and checks if it contains any tasks "
        "with status of CANCELED / COMPLETED_WITH_ERRORS / FAILED / FAILED_WITH_TERMINAL_ERROR / "
        "SKIPPED / TIMED_OUT. If propagate_fails is specified this task will fail as well,"
        "return_failed_tasks_data will returns all failed sub-workflow data.",
    ),
)
def check_recursively_if_has_failed_task(
    workflow_id: str, propagate_fail: bool | None = False, return_failed_tasks_data: bool | None = False
) -> TaskResult:
    workflow_data_tree = build_workflow_data_tree(workflow_id)
    error_data = workflow_data_tree.build_error_tree()

    if error_data.is_failed_status() or error_data.failed_children:
        status = TaskResultStatus.FAILED if propagate_fail else TaskResultStatus.COMPLETED
    else:
        status = TaskResultStatus.COMPLETED

    return TaskResult(status=status, output_data=error_data)
