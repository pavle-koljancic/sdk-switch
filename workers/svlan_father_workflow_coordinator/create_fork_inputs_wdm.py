import json
from typing import Any

from conductor.client import worker_task

from models.fork.dynamic_fork_inputs import DynamicForkInputs


@worker_task(
    task_definition_name="create_fork_inputs_wdm",
    register_task_def=True,  # Auto-register on startup
)
def create_fork_inputs_wdm(paths: list[dict[str, str]], svlan: str | int, pop_collect: str) -> DynamicForkInputs:
    # Temporary workaround: when run from the definition, the 'paths' input is a string,
    # but when executed as a rerun, the same very same input is a list.
    if isinstance(paths, str):
        paths = json.loads(paths)
    ###

    if isinstance(svlan, int):
        svlan = str(svlan)

    fork_id = 1
    dynamic_tasks = []  # Initialize an empty list to hold dynamically generated tasks.
    dynamic_tasks_input: dict[str, Any] = {}  # Initialize an empty dictionary to hold information about path pairs.

    for path in paths:
        wfs_to_run = ("Discover_SVLANs_configurations_WDM", "Prepare_service_configuration_deletion_nso_WDM")

        for workflow_name in wfs_to_run:
            fork_key = f"{workflow_name}_fork_{fork_id}"

            dynamic_tasks_input[fork_key] = {
                "path_from": f"{path.get('path_from')}",
                "path_to": f"{path.get('path_to')}",
                "svlan": svlan,
                "pop_collect": pop_collect,
                "fork_id": fork_id,
            }
            dynamic_tasks.append(
                {
                    "name": f"sub_task_{fork_id}",
                    "taskReferenceName": fork_key,
                    "type": "SUB_WORKFLOW",
                    "optional": True,
                    "subWorkflowParam": {"name": workflow_name, "version": "1"},
                }
            )
        fork_id += 1

    return DynamicForkInputs(dynamic_tasks_input=dynamic_tasks_input, dynamic_tasks=dynamic_tasks)
