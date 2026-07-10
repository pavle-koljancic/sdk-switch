from typing import Annotated
from typing import Any

from pydantic import BaseModel
from pydantic import BeforeValidator
from pydantic import computed_field

from models.db_nso.kit_entity import KitEntity
from models.db_nso.status_svlan_entity import StatusSvlanEntity
from models.router.router_interfaces import bandwidth_type_mapping


def kit_entity_validator(kit: KitEntity | None | dict[str, Any]) -> KitEntity:
    if not kit:
        return KitEntity(nome_kit="N/A", equipment="N/A", porta="N/A")

    if isinstance(kit, KitEntity):
        kit_dict = kit.model_dump()

        kit_dict["id_kit"] = kit_dict.get("id_kit", "N/A")
        kit_dict["equipment"] = kit_dict.get("equipment", "N/A")
        kit_dict["porta"] = kit_dict.get("porta", "N/A")
        kit_dict["bandwidth"] = kit_dict.get("bandwidth", "N/A")

        return KitEntity(**kit_dict)

    if isinstance(kit, dict):
        return KitEntity(**kit)

    raise TypeError(f"Invalid type for 'kit': {type(kit).__name__}. Expected KitEntity, dict, or None.")


class SvlanExtractionOutput(BaseModel):
    status_svlan: StatusSvlanEntity
    kit: Annotated[
        KitEntity,
        BeforeValidator(kit_entity_validator),
    ]
    users: list[str]

    @computed_field
    def interface_type(self) -> str:
        key = self.kit.bandwidth or "default_key"
        return bandwidth_type_mapping.get(key, "N/A")
