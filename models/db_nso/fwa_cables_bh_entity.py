from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class FwaCablesBhEntity(DbBaseEntity):
    pop: str | None = None
    fwa_srb: str | None = None
    wdm_name: str | None = None
    wdm_slot_1: str | None = None
    wdm_port_1: str | None = None
    wdm_slot_2: str | None = None
    wdm_port_2: str | None = None
    type: str | None = None
    svlan_operator: str | None = None
    router_c: str | None = None
    router_c_slot: str | None = None
    router_c_port: str | None = None
    data_insert: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    table_name: ClassVar[str] = "nso.eng_fwa_cables_bh"
