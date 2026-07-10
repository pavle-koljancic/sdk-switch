from functools import lru_cache
from itertools import dropwhile
from typing import Annotated

from pydantic import AfterValidator
from pydantic.dataclasses import dataclass

from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


def _validate_unipkt(value: str) -> str:
    shelves_slots_ports = CsvSiaeUni._extract_wdm_shelf_slot_ports(value)
    if len(shelves_slots_ports) > 0:
        return value
    raise ValueError(f"No shelf/slot/port could be extracted from unipkt_port:{value}")


# Data model for SIAE_UNI_CSV_FILE
@dataclass(frozen=True)
class CsvSiaeUni:
    # Name of the wdm(SIAE) device
    equipment_name: str
    # String containing the shelf_slot_port data
    unipkt_port: Annotated[str, AfterValidator(_validate_unipkt)]
    # Name of te interface
    uni_interface_name: str
    interface_type: str

    @property
    def shelf_slot_port(self) -> set[WdmShelfSlotPort]:
        return CsvSiaeUni._extract_wdm_shelf_slot_ports(self.unipkt_port)

    @classmethod
    @lru_cache(maxsize=512)
    def _extract_wdm_shelf_slot_ports(cls, unipkt_port: str) -> set[WdmShelfSlotPort]:
        result_set: set[WdmShelfSlotPort] = set()
        list_shelf_slot_port = list(
            dropwhile(lambda slice: not WdmShelfSlotPort.is_valid_shelf(slice), unipkt_port.split("-"))
        )

        # If the list of extract shelf slot ports is empty or not devisable by 3 then extraction failed
        # It must be devisable by 3 because each group of 3 is a shelf/slot/port combination

        if not list_shelf_slot_port or len(list_shelf_slot_port) % WdmShelfSlotPort.num_of_ports_full != 0:
            raise ValueError(f"Failed to extract shelf/slot/port from unipkt_port:{unipkt_port}")

        for index in range(0, len(list_shelf_slot_port), WdmShelfSlotPort.num_of_ports_full):
            result_set.add(
                WdmShelfSlotPort(
                    shelf=list_shelf_slot_port[index],
                    slot=list_shelf_slot_port[index + 1],
                    port=list_shelf_slot_port[index + 2],
                )
            )
        return result_set
