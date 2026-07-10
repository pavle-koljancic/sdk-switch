from enum import IntEnum
from typing import Annotated

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import StringConstraints
from pydantic import model_serializer

from models.db_nso.kit_entity import KitEntity
from models.router.router_interfaces import bandwidth_type_mapping
from models.wdm.wdm_device_vendor import WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS
from models.wdm.wdm_device_vendor import WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS


# Enum used because magic numbers are not allowed by mypy
class InterfaceNumberLength(IntEnum):
    # Virtual/logical interface Port-Channel for cisco-ios and Bundle-Id for cisco-ios-xr
    LOGICAL = 1
    # cisco-ios physical with the leading zero missing. Example: 2/3
    CISCO_IOS_PARTIAL_PHYSICAL = 2
    # cisco-ios physical. Example: 0/2/3
    CISCO_IOS_PHYSICAL = 3
    # cisco-ios-xr physical. Example: 0/1/2/3
    CISCO_IOS_XR_PHYSICAL = 4


def _is_kit_on_wdm(equipment: str) -> bool:
    matched_huawei = [sub for sub in WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS if sub in equipment]
    matched_uni = [sub for sub in WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS if sub in equipment]
    return bool(matched_huawei or matched_uni)


def _all_digits(parts: list[str]) -> bool:
    return all(s.isdigit() for s in parts)


def _validate_interface_number(interface_number: str) -> str:
    split_interface = interface_number.split("/")

    if not _all_digits(parts=split_interface):
        raise ValueError(f"Invalid interface_number:{interface_number}")

    match len(split_interface):
        case (
            InterfaceNumberLength.CISCO_IOS_PHYSICAL
            | InterfaceNumberLength.CISCO_IOS_XR_PHYSICAL
            | InterfaceNumberLength.LOGICAL
        ):
            return interface_number

        case InterfaceNumberLength.CISCO_IOS_PARTIAL_PHYSICAL:
            # It was stated by the clients
            # if we get only 2 numbers for the interface_number
            # that we should add a leading 0
            return f"0/{interface_number}"

        case _:
            raise ValueError(f"Invalid interface_number:{interface_number}")


def _validate_bandwidth_mapping(bandwidth: str) -> str:
    if bandwidth.upper() not in bandwidth_type_mapping:
        raise ValueError("Could not map bandwidth to interface type.")
    return bandwidth


class RouterDeliveryDTO(KitEntity):
    model_config = ConfigDict(frozen=True)

    equipment: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    porta: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1), BeforeValidator(_validate_interface_number)
    ]
    bandwidth: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1), BeforeValidator(_validate_bandwidth_mapping)
    ]

    @model_serializer(mode="plain")
    def serialize_model(self) -> dict[str, object]:
        return {
            "router_name": self.equipment,
            "interface_number": self.porta,
            "interface_type": bandwidth_type_mapping.get(self.bandwidth.upper()),
            "kit_on_wdm": _is_kit_on_wdm(self.equipment),
        }
