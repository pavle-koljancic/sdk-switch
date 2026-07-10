from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict


@dataclass(frozen=True)
class Select:
    expression: str
    label: str = ""
    result_type: Literal["string", "inline"] = "string"

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "expression": self.expression,
            "result-type": [self.result_type],
        }

    def for_field(self, field_name: str) -> "Select":
        return Select(
            expression=self.expression,
            label=self.label or field_name,
            result_type=self.result_type,
        )


def _get_select_metadata(metadata: Iterable[Any]) -> Select | None:
    for item in metadata:
        if isinstance(item, Select):
            return item
    return None


class NsoBaseResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    @classmethod
    def _field_selects(cls) -> tuple[Select, ...]:
        resolved: list[Select] = []

        for field_name, field_info in cls.model_fields.items():
            select = _get_select_metadata(field_info.metadata)
            if select is None:
                raise TypeError(f"{cls.__name__}.{field_name} must include Select annotation")
            resolved.append(select.for_field(field_name))

        return tuple(resolved)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)

        if cls is NsoBaseResult:
            return

        cls._field_selects()

    @classmethod
    def selects(cls) -> tuple[Select, ...]:
        return cls._field_selects()
