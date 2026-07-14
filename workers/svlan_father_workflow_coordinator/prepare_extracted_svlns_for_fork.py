from typing import Any

from conductor.client import worker_task

from models.fork.dynamic_fork_inputs import DynamicForkInputs
from models.svlan_extraction.svlan_extraction_output import SvlanExtractionOutput
from conductor.client.http.models.task_def import TaskDef


@worker_task(
    task_definition_name="prepare_extracted_svlns_for_fork",
    register_task_def=True,  # Auto-register on startup
    task_def=TaskDef(
                    description="Create tasks and input data for dynamic forks to run sub-workflows from the WDM layer.",
            timeout_seconds=  180)
)
def prepare_extracted_svlns_for_fork(
    extracted_svlan_outputs: list[SvlanExtractionOutput],
    interface_number_collect: str,
    interface_type_collect: str,
    router_collect: str,
    pop_standard: str,
    pop_exception: str,
    new_trunk: str,
    paths: list[dict[str, str]],
) -> DynamicForkInputs:
    dynamic_tasks = []  # Initialize an empty list to hold dynamically generated tasks.
    fork_id = 1  # Initialize a variable to keep track of unique IDs for forks.
    svlans: dict[str, Any] = {}  # Initialize an empty dictionary to hold information about svlans.

    # Sorting the svlans so that from now on the order is deterministic.
    # If the svlan is missing it sorts it as 0
    extracted_svlan_outputs.sort(
        key=lambda extracted_output: extracted_output.status_svlan.svlan if extracted_output.status_svlan.svlan else 0
    )

    for extracted_output in extracted_svlan_outputs:  # Iterate over each extracted svlan
        fork_key = f"fork_run_all_wfs_svlan_{extracted_output.status_svlan.svlan}_fork_id_{fork_id}"

        svlans[fork_key] = {
            "svlan": extracted_output.status_svlan.svlan,
            "interface_type_delivery": extracted_output.interface_type,
            "interface_number_delivery": extracted_output.kit.porta,
            "router_delivery": extracted_output.kit.equipment,
            "id_kit": extracted_output.kit.id_kit,
            "svlan_mode_type": extracted_output.status_svlan.mode,
            "olo": extracted_output.status_svlan.olo,
            "resource_id": extracted_output.status_svlan.resource_id,
            "pop_standard": pop_standard,
            "pop_exception": pop_exception,
            "paths": paths,
            "interface_type_collect": interface_type_collect,
            "interface_number_collect": interface_number_collect,
            "router_collect": router_collect,
            "new_trunk": new_trunk,
            "nome_kit": extracted_output.kit.nome_kit,
        }

        dynamic_tasks.append(
            {
                "name": f"sub_task_{fork_id}",
                "taskReferenceName": fork_key,
                "type": "SUB_WORKFLOW",
                "optional": True,
                "subWorkflowParam": {"name": "SVLAN_workflow_coordinator_run_for_single_SVLAN", "version": "1"},
            }
        )
        fork_id += 1

    return DynamicForkInputs(dynamic_tasks_input=svlans, dynamic_tasks=dynamic_tasks)
