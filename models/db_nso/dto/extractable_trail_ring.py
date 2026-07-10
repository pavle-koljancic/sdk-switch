from typing import Any

from pydantic import model_validator

from models.db_nso.trail_ring_entity import TrailRingEntity
from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


# Model based on trail ring entity used for validating and extracting necessary data
class ExtractableTrailRingDTO(TrailRingEntity):
    nome_wdm_3: str
    nome_wdm_4: str
    router_pe1: str
    ifc_router_pe1: str
    ifc_wdm_3: str
    ifc_wdm_4: str

    @property
    def ifc_3__shelf_slot_port(self) -> WdmShelfSlotPort:
        return WdmShelfSlotPort.from_str(self.ifc_wdm_3)

    @property
    def ifc_4__shelf_slot_port(self) -> WdmShelfSlotPort:
        return WdmShelfSlotPort.from_str(self.ifc_wdm_4)

    @model_validator(mode="before")
    @classmethod
    def parse_ports(cls, data: dict[str, Any]) -> dict[str, Any]:
        # The call is used to validate the values in ifc_wdm_3 and ifc_wdm_4
        WdmShelfSlotPort.from_str(data["ifc_wdm_3"])
        WdmShelfSlotPort.from_str(data["ifc_wdm_4"])
        return data
