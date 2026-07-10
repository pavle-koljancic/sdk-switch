from enum import StrEnum


class CiscoIOSInterface(StrEnum):
    Te = "TenGigabitEthernet"
    Ge = "GigabitEthernet"
    Hu = "HundredGigE"


class CiscoIOSXrInterface(StrEnum):
    Te = "TenGigE"
    Ge = "GigabitEthernet"
    Hu = "HundredGigE"


bandwidth_type_mapping = {"1GB": "Ge", "10GB": "Te", "100GB": "Hu"}
