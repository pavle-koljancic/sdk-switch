import logging
from datetime import datetime
from typing import Any
from typing import ClassVar

from pydantic import BaseModel


def _validate_svlan(svlan: Any) -> int | None:
    if svlan is None:
        return svlan

    if isinstance(svlan, int) and svlan >= 0:
        return svlan

    if isinstance(svlan, str) and svlan.isdigit():
        return int(svlan)

    raise ValueError("Conversion not possible svlan passed must be None or a str convertible to a Non-negative int")


def _validate_pop_collect(pop: str) -> str:
    if not pop or not pop.strip():
        raise ValueError("pop_collect must not be empty or blank")

    return pop


def convert_str_to_datetime(dt: Any) -> datetime | None:
    if dt is None or isinstance(dt, datetime):
        return dt
    if isinstance(dt, str):
        return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")

    raise ValueError(f"Conversion not possible for {type(dt)}")


def serialize_date_time_to_str(data_insert: datetime) -> str:
    return data_insert.strftime("%Y-%m-%d %H:%M:%S.%f")


logger = logging.getLogger(__name__)


class DbBaseEntity(BaseModel):
    ENTITY_REGISTRY: ClassVar[dict[str, type["DbBaseEntity"]]] = {}

    def __init_subclass__(cls: type["DbBaseEntity"], **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        DbBaseEntity.ENTITY_REGISTRY[cls.__name__] = cls
        logger.info(
            "Registered DB entity: %s (table=%s)",
            cls.__name__,
            getattr(cls, "table_name", "N/A"),
        )

    table_name: ClassVar[str | None] = None
