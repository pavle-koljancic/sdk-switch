from typing import ClassVar

from pydantic import ConfigDict

from models.db_nso.db_base_entity import DbBaseEntity


class PopExceptionEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)
    pop_exception: str | None = None
    pop_standard: str | None = None
    table_name: ClassVar[str] = "nso.eng_pop_exception"
