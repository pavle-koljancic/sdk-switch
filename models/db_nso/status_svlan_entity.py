from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import _validate_svlan
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class StatusSvlanEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)
    olo: str | None = None
    pop_collect: str | None = None
    pop_rif: str | None = None
    svlan: Annotated[int | None, BeforeValidator(_validate_svlan)] = None
    svlan_translation_olo: Annotated[int | None, BeforeValidator(_validate_svlan)] = None
    cos: str | None = None
    kit: str | None = None
    resource_id: str | None = None
    mode: str | None = None
    auth: str | None = None
    trunk: str | None = None
    data_insert: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    phase: str | None = None
    table_name: ClassVar[str] = "nso.eng_status_svlan"
