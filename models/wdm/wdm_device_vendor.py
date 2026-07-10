from enum import Enum

WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS = ["1800V", "U16", "1800II", "M24"]
WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS = ["1OTN", "1830ONE", "Edge-B", "Hub"]


# Enum used for representing the possible WDM vendors in OpenFibers system
class WDMDeviceVendor(Enum):
    HUAWEI = "HUAWEI"
    SIAE = "SIAE"

    # Method for determining vendor from wdm device name
    @classmethod
    def get_vendor_from_device_name(cls, device_name: str) -> "WDMDeviceVendor":
        if any(sub_str in device_name for sub_str in WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS):
            return WDMDeviceVendor.HUAWEI
        if any(sub_str in device_name for sub_str in WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS):
            return WDMDeviceVendor.SIAE

        raise ValueError(f"No wdm vendor for device_name:{device_name}")
