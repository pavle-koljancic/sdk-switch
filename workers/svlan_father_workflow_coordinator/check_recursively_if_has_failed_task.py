from conductor.client import TaskResult
from conductor.client import TaskResultStatus
from conductor.client import worker_task

from helper.wf_loader_v2 import build_workflow_data_tree


@worker_task(
    task_definition_name="check_recursively_if_has_failed_task",
    register_task_def=True,  # Auto-register on startup
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
