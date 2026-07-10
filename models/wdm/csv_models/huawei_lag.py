from pydantic.dataclasses import dataclass


# Data model for HUAWEI_LAG_CSV_FILE
# The HUAWEI_LAG_CSV_FILE is a record of all Link Aggregation Groups(LAG)
# A Link Aggregation Group  is a grouping of physical ports to form one larger virtual connection
# One row maps to this model
@dataclass(frozen=True)
class CsvHuaweiLag:
    node_a: str  # the device name
    string_11_31: str  # Just a constant that always says 11-31
    meid_node_a: str  # device_id (It is unclear now if this ID is bound to the device or the device and lag)
    primary_port: str  # primary interface of the device in the lag
    meid_node_b: str  # This should always be equal to meid_node_a
    backup_port: str | None  # backup interface of the device in the lag
    ethtrunk_port: str | None  # ethernet interface
