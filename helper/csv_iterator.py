import csv
import os
from collections.abc import Iterator
from dataclasses import is_dataclass
from typing import TypeVar

from pydantic import ValidationError

from helper.utils import resolve_host_path
from task_logging.task_logger import get_task_logger

T = TypeVar("T")

task_logger = get_task_logger()


def iterator(csv_name: str, delimiter: str, dataclass_type: type[T], logging: bool = True) -> Iterator[T]:
    csv_location: str | None = os.environ.get(csv_name)

    """
    Generic CSV loader that yields instances of ANY pydantic dataclass.

    Args:
        dataclass_type: The pydantic dataclass to instantiate for each row.
        csv_name: Name of the environment variable holding the CSV path.
        delimiter: CSV delimiter, defaults to ';'.

    Yields:
        Instances of dataclass_type.
    """

    if not csv_location:
        raise OSError(f"Could not find CSV location. Environment variable '{csv_name}' must be set.")

    if not is_dataclass(dataclass_type):
        raise TypeError("dataclass_type must be a pydantic dataclass")

    fieldnames = list(dataclass_type.__dataclass_fields__.keys())

    with open(csv_location, newline="") as csv_file:
        task_logger.info("Opened CSV: %s\nColumns: %s", resolve_host_path(csv_location), fieldnames)
        csv_reader = csv.DictReader(
            csv_file,
            delimiter=delimiter,
            fieldnames=fieldnames,
            restkey="_extra",  # if more columns are read the expected they will be here.
        )
        for row_dict in csv_reader:
            try:
                yield dataclass_type(**row_dict)
            except ValidationError as error:
                if logging:
                    task_logger.warning(
                        f"{csv_location} Invalid data, skipping line:{csv_reader.line_num}\n{error.errors()[0]['msg']}"
                    )
            continue
