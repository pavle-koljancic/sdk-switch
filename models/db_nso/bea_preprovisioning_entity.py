from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import _validate_svlan


class BeaPreprovisioningEntity(DbBaseEntity):
    table_name: ClassVar[str] = "nso.bea_preprovisioning"
    resource_id: str | None = None
    pop_name: str | None = None
    svlan: Annotated[int | None, BeforeValidator(_validate_svlan)] = None
    starting_equipment: str | None = None
    interface: str | None = None
