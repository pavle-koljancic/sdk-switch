from typing import ClassVar

from pydantic import ConfigDict

from models.db_nso.db_base_entity import DbBaseEntity


class EngProfileTableBeaEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    profile_id: int | None = None
    pir: int | None = None
    cos0: int | None = None
    cos1: int | None = None
    cos3: int | None = None
    cos5: int | None = None
    eir_y1564: int | None = None

    table_name: ClassVar[str] = "nso.eng_profile_table_bea"
