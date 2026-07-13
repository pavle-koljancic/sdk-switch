from dataclasses import dataclass
from typing import Any


@dataclass
class DynamicForkInputs:
    dynamic_tasks_input: dict[str, Any]
    dynamic_tasks: list[Any]
