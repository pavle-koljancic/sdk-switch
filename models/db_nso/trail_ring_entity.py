from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class TrailRingEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    nome_wdm_3: str | None = None
    ifc_wdm_3: str | None = None
    nome_wdm_4: str | None = None
    nome_ring: str | None = None
    router_pe1: str | None = None
    ifc_router_pe1: str | None = None
    status: str | None = None
    ifc_wdm_4: str | None = None

    data_insert: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(
            func=serialize_date_time_to_str,
            return_type=str,
            when_used="unless-none",
        ),
    ] = None

    table_name: ClassVar[str] = "nso.eng_trail_ring"
