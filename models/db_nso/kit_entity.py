from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class KitEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    nome_kit: str | None = None
    id_kit: str | None = None
    equipment: str | None = None
    pop: str | None = None
    porta: str | None = None
    olo: str | None = None
    bandwidth: str | None = None
    note: str | None = None
    data_insert: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    kit_type: str | None = None

    table_name: ClassVar[str] = "nso.eng_kit"
