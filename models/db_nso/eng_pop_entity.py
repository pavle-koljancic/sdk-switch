from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class EngPopEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    pop_collect: str | None = None
    type: str | None = None
    link: str | None = None
    pop_rif: str | None = None
    pop_rif_type: str | None = None
    pop_nazionale: str | None = None
    trunk: str | None = None
    technology_trunk: str | None = None

    data_insert: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(
            func=serialize_date_time_to_str,
            return_type=str,
            when_used="unless-none",
        ),
    ] = None

    bng: str | None = None
    trunk_old: str | None = None

    table_name: ClassVar[str] = "nso.eng_pop"
