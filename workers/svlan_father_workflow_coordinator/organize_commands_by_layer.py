from typing import Any

from conductor.client import worker_task
from conductor.client.http.models.task_def import TaskDef


def aggregate_commands_by_layer(
    data: dict[str, Any],
    result: dict[str, Any] | None = None,
    target_layers: list[str] = ["OLT_LAYER", "ROUTER_LAYER", "WDM_layer"],
) -> dict[str, Any]:
    if result is None:
        result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if key in target_layers:
                if key not in result:
                    result[key] = []
                collect_commands(value, result[key])
            else:
                aggregate_commands_by_layer(value, result, target_layers)

    return result


def collect_commands(data: dict[str, Any] | list[Any] | str, result: list[Any]) -> None:
    if isinstance(data, dict):
        if "commands" in data:
            # Directly check for commands and format them
            command_data = data["commands"]
            if isinstance(command_data, dict | list):
                # If commands are in a dict or list, convert to a string representation
                flatten_command_data(command_data, result)
            else:
                result.append(command_data)
        else:
            for value in data.values():
                collect_commands(value, result)
    elif isinstance(data, list):
        for item in data:
            collect_commands(item, result)
    elif isinstance(data, str):
        result.append(data)


def flatten_command_data(data: dict[str, Any] | list[Any], result: list[str]) -> None:
    # Function to flatten and convert complex nested structures into strings
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        # Convert dict to string by extracting all values and concatenating
                        command = " ".join([str(v) for v in item.values()])
                        result.append(command)
                    else:
                        result.append(str(item))
            else:
                result.append(f"{key} {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                flatten_command_data(item, result)
            else:
                result.append(str(item))


@worker_task(
    task_definition_name="organize_commands_by_layer",
    register_task_def=True,  # Auto-register on startup
)
def organize_commands_by_layer(all_commands: dict[str, Any]) -> dict[str, Any]:
    commands_by_layer: dict[str, Any] = aggregate_commands_by_layer(all_commands)

    return commands_by_layer
