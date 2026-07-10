import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from conductor.client import worker_task

from helper.timestamp_utils import generate_timestamp
from helper.timestamp_utils import get_workflow_data
from helper.utils import resolve_host_path
from task_logging.task_logger import get_task_logger

task_logger = get_task_logger()


@dataclass
class WorkerOutput:
    output_file_path: str | None
    saved: bool = False


@worker_task(
    task_definition_name="export_to_local_disk",
    register_task_def=True,  # Auto-register on startup
)
def export_to_local_disk(
    file_name: str,
    filetype: str,
    workflow_id: str,
    pop_name: str,
    directory: str | int,
    fields: list[str],
    data_to_save: object,
) -> WorkerOutput:
    output_file_path: str | None = None
    is_saved: bool = False

    if isinstance(directory, int):
        directory = str(directory)

    filetype = filetype.lower()
    if filetype not in ["txt", "json", "csv", "bash"]:
        raise NotImplementedError(f"File type '{filetype}' not supported. Supported types")

    workflow_data: dict[str, Any] = get_workflow_data(workflow_id)

    while workflow_data and workflow_data.get("parentWorkflowId"):
        parent_id = workflow_data["parentWorkflowId"]
        task_logger.info(f"Parent workflow ID: {parent_id}")
        workflow_data = get_workflow_data(parent_id)

    timestamp = generate_timestamp(workflow_data.get("createTime", None))

    if data_to_save is not None:
        try:
            file_name = file_name.replace("/", "_")
            pop_name = pop_name.replace("/", "_")
            directory = directory.replace("/", "_")

            # Create directory structure
            folder_path: Path = Path("fm_outputs") / f"{timestamp}-{pop_name}" / directory
            folder_path.mkdir(parents=True, exist_ok=True)

            # Format data based on type and filetype
            if filetype == "bash":
                data_string = _to_bash(data_to_save)

            elif filetype == "csv":
                data_string = _to_csv(data_to_save, fields)
            elif filetype == "json" and (data_to_save, (list | dict)):
                data_string = json.dumps(data_to_save, indent=4, sort_keys=True, ensure_ascii=False)
            elif isinstance(data_to_save, list):
                data_string = "\n".join(map(str, data_to_save))
            elif isinstance(data_to_save, dict):
                data_string = "\n".join(f"{k}: {v}" for k, v in data_to_save.items())
            else:
                data_string = str(data_to_save)

            # Construct file path and write data
            file_path = folder_path / f"{file_name}.{filetype}"
            with open(file_path, "w", encoding="utf-8") as outfile:
                outfile.write(data_string if data_string.endswith("\n") else data_string + "\n")

            _output_file_path = str(file_path.resolve())
            output_file_path = resolve_host_path(_output_file_path)
            is_saved = True
            task_logger.info(f"Successfully saved data to: {output_file_path}")

        except OSError as e:
            error_msg = f"Failed to save file: {e}"
            task_logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    return WorkerOutput(
        saved=is_saved,
        output_file_path=output_file_path,
    )


def _dict_to_csv_line(d: dict[str, Any], fields: list[str], delimiter: str = ";", sub_delimiter: str = ",") -> str:
    missing = [f for f in fields if f not in d]
    if missing:
        raise ValueError(f"Dictionary is missing required fields: {missing}")

    values = []
    for field in fields:
        val = d.get(field, "")
        if isinstance(val, list | tuple):
            val = sub_delimiter.join(str(v) for v in val)
        values.append(str(val))

    return delimiter.join(values)


def _to_csv(data_to_save: Any, fields: list[str], delimiter: str = ";") -> str:
    if isinstance(data_to_save, list):
        data: list[str] = list(
            map(
                lambda item: _dict_to_csv_line(item, fields, delimiter),
                data_to_save,
            )
        )

        # build headers and insert at beginning
        data.insert(0, delimiter.join(fields))
        return "\n".join(data)
    if isinstance(data_to_save, dict):
        return "\n".join(
            [
                delimiter.join(fields),
                _dict_to_csv_line(data_to_save, fields),
            ]
        )
    raise ValueError("CSV export expects a list or dict as data_to_save")


def _to_bash(data_to_save: Any) -> str:
    commands: list[str] = []
    stack = []
    stack.append(data_to_save)

    while len(stack) > 0:
        next_node = stack.pop()

        as_list: list[Any] | None = None

        if isinstance(next_node, str):
            commands.append(next_node)
        elif isinstance(next_node, list):
            as_list = next_node
        elif isinstance(next_node, dict):
            as_list = list(next_node.values())
        else:
            raise Exception("Couldn't extract commands")
        if as_list is not None:
            stack.extend(reversed(as_list))

    return "\n".join(commands)
