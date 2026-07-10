from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class EngBhCablesEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    pop: str | None = None
    olt_name: str | None = None
    ifc_olt: str | None = None

    nome_wdm_1: str | None = None
    ifc_wdm_1_collect: str | None = None
    ifc_wdm_1_delivery: str | None = None

    type: str | None = None
    svlan_operator: str | None = None

    router_pe1: str | None = None
    ifc_router_pe1: str | None = None
    ifc_router_type: str | None = None

    data_insert: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(
            func=serialize_date_time_to_str,
            return_type=str,
            when_used="unless-none",
        ),
    ] = None

    operatore: str | None = None

    table_name: ClassVar[str] = "nso.eng_bh_cables"
