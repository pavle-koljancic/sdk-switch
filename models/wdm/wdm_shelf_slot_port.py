import re
from functools import lru_cache
from typing import Annotated
from typing import ClassVar

from pydantic import BaseModel
from pydantic import BeforeValidator
from pydantic import ConfigDict


def _validate_slot(slot: int | str) -> str:
    if isinstance(slot, int) and slot >= 0:
        return str(slot)

    if isinstance(slot, str) and slot.isdigit():
        return slot

    raise ValueError(f"Slot value incorrect:{slot}, must be a Non-negative int .")


def _validate_port(port: int | str) -> str:
    if isinstance(port, int) and port >= 0:
        return str(port)

    if isinstance(port, str) and port.isdigit():
        return port

    raise ValueError(f"Port value incorrect:{port}, must be a Non-negative int .")


# shelf can start with p and can be of the form p1 p2 and so on.
def _validate_shelf(shelf: int | str) -> str:
    if isinstance(shelf, int) and shelf >= 0:
        return str(shelf)

    if isinstance(shelf, str) and (WdmShelfSlotPort.is_valid_shelf(shelf)):
        return shelf

    raise ValueError(f"Shelf value incorrect:{shelf} must be Non-negative int, can start with on 'p' before int.")


# Model used for representing the shelf/slot/port of wdm devices
# EXAMPLE_DEVICE 1/2/3 -> Shelf:1 Slot:2 Port:1
# Shelves can start with p so p1 is a valid shelf value
# All shelf, slot, numbers must be valid digits(Non negative int)
class WdmShelfSlotPort(BaseModel):
    model_config = ConfigDict(frozen=True)
    shelf: Annotated[str, BeforeValidator(_validate_shelf)]
    slot: Annotated[str, BeforeValidator(_validate_slot)]
    port: Annotated[str, BeforeValidator(_validate_port)]

    num_of_ports_full: ClassVar[int] = 3  # In case the shelf/slot/port is specified as 1/2/3
    num_of_ports_short: ClassVar[int] = (
        2  # In case the shelf/slot/port is specified as 2/1 in that case  shelf is 0 by default
    )

    def format_primary_slot_port(self) -> str:
        """
        Given slot and port, return the primary string used in CSV comparison.
        Example: slot=11, port=2 -> "primary:slot=11-port=2"
        """
        return f"primary:slot={self.slot}-port={self.port}"

    # Method used for extracting the shelf/slot/port value from a string '1/2/3'
    # If there is only 2 values in the string (HUAWEI) Shelf:0
    @classmethod
    @lru_cache(maxsize=512)
    def from_str(cls, input_str: str, separator: str = "/") -> "WdmShelfSlotPort":
        if input_str is None:
            return ValueError("Input string for shelf_slot_port missing!")

        values = input_str.split(separator)
        if len(values) == WdmShelfSlotPort.num_of_ports_full:
            return WdmShelfSlotPort(shelf=values[0], slot=values[1], port=values[2])
        if len(values) == WdmShelfSlotPort.num_of_ports_short:
            return WdmShelfSlotPort(shelf="0", slot=values[0], port=values[1])

        if len(values) > WdmShelfSlotPort.num_of_ports_full:
            raise ValueError(f"To many numbers. shelf/slot/port can be 3 values at most. Value:{str} ")
        raise ValueError(f"Missing values. shelf/slot/port must be at least 2 values. Value:{str} ")

    @classmethod
    @lru_cache(maxsize=512)
    def from_formatted_string(cls, input_str: str) -> "WdmShelfSlotPort":
        if input_str is None:
            return ValueError("Input string for shelf_slot_port missing!")

        pattern = r"shelf=(?P<shelf>\d+)-slot=(?P<slot>\d+)-port=(?P<port>\d+)"
        match = re.match(pattern, input_str.strip())
        if not match:
            raise ValueError(
                f"Input string not in expected format 'shelf=X-slot=Y-port=Z' with numeric values. Got: {input_str}"
            )

        return cls(
            shelf=match.group("shelf"),
            slot=match.group("slot"),
            port=match.group("port"),
        )

    def shelf_slot_port_string(self) -> str:
        return f"shelf={self.shelf}-slot={self.slot}-port={self.port}"

    def minus_string(self) -> str:
        return f"{self.shelf}-{self.slot}-{self.port}"

    @classmethod
    def is_valid_shelf(cls, shelf: str) -> bool:
        return shelf.isdigit() or (shelf.startswith("p") and shelf[1:].isdigit())
