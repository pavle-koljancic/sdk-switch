from typing import Annotated
from typing import Any
from typing import cast

from pydantic import AfterValidator
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import PlainSerializer
from pydantic import SerializerFunctionWrapHandler
from pydantic import model_serializer
from pydantic import model_validator

from models.wdm.wdm_device_vendor import WDMDeviceVendor
from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


# Checks if the WdmVendor(Enum) can be extracted from the WdmDevice name
def validate_vendor(v: str) -> str:
    try:
        WDMDeviceVendor.get_vendor_from_device_name(v)
    except Exception as e:
        raise ValueError(f"Invalid device name '{v}': cannot determine vendor") from e
    return v


# Model representing a Wdm Device (SIAE/HUAWEI)
class WdmDevice(BaseModel):
    model_config = ConfigDict(frozen=True)
    # name of the device
    name: Annotated[str, AfterValidator(validate_vendor)] = Field(min_length=1)
    # Set of shelves/slots/ports on the given device.
    # Ex: '1/2/3 p4/5/6' [{shelf=1 slot=2 port=3},{shelf=p4 slot=5 port=6}]
    shelves_slots_ports: Annotated[set[WdmShelfSlotPort], PlainSerializer(list, return_type=list)] = Field(min_length=1)
    # If none is specified it is assumed to be the first one provided by default
    primary_shelf_slot_port: WdmShelfSlotPort

    @property
    def vendor(self) -> WDMDeviceVendor:
        return WDMDeviceVendor.get_vendor_from_device_name(self.name)

    @classmethod
    def from_path_str(cls, path_str: str) -> "WdmDevice":
        """Extracts  WdmDevice (device_name, set[shelf/port/slot]) from a path given as input.
        These are used to filter entries (WDM) inside CSV files.
        Each shelf/port/slot combination is converted to its WdmShelfSlotPort model

        Args:
            path (str): The path containing details.

        Returns:
            WdmDevice
        """
        # split path on ' '
        min_length = 2
        path_split = path_str.split()
        if len(path_split) < min_length:
            raise ValueError(f"Missing name or shelf/slot/port from path:{path_str}")
        wdm_device_name = path_split[0]

        shelves_slot_ports_str: list[str] = path_split[1:]

        # Checks if any of the shelves slot ports starts with a "/"
        if any([item.startswith("/") for item in shelves_slot_ports_str]):
            if WDMDeviceVendor.get_vendor_from_device_name(wdm_device_name) == WDMDeviceVendor.HUAWEI:
                shelves_slot_ports_str = list(
                    map(lambda shelf_slot_port: shelf_slot_port.lstrip("/"), shelves_slot_ports_str)
                )
            else:
                raise ValueError("Only HUAWEI device may start with a leading /")
        return WdmDevice(
            name=wdm_device_name,
            shelves_slots_ports=set(map(WdmShelfSlotPort.from_str, shelves_slot_ports_str)),
            primary_shelf_slot_port=WdmShelfSlotPort.from_str(shelves_slot_ports_str[0]),
        )

    # used for proper serialization of vendor
    # Pydantic.v2 has problems when it comes to enum serialization
    @model_serializer(mode="wrap")
    def serialize_model(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        serialized: dict[str, object] = handler(self)
        serialized["vendor"] = self.vendor
        return serialized

    # added so that if no primary port is specified the first one will be taken
    @model_validator(mode="before")
    @classmethod
    def set_default_primary(cls, data: dict[str, Any]) -> dict[str, Any]:
        if isinstance(data, dict):
            # In the case the primary shelf slot port is not set the first one is selected as the primary
            if "primary_shelf_slot_port" not in data or data["primary_shelf_slot_port"] is None:
                ports = data.get("shelves_slots_ports")
                if ports:
                    # The selection is non deterministic
                    data["primary_shelf_slot_port"] = next(iter(ports))
        return data

    @model_validator(mode="after")
    def check_primary_is_member(self: "WdmDevice") -> "WdmDevice":
        if self.primary_shelf_slot_port not in self.shelves_slots_ports:
            raise ValueError("Primary shelf slot port not a member of the set")
        return self
