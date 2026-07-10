from typing import Annotated
from typing import Any

from pydantic import BeforeValidator
from pydantic import model_validator
from pydantic.dataclasses import dataclass

from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


def _normalize_wdm_ports(input_port: Any) -> WdmShelfSlotPort:
    if isinstance(input_port, str):
        return WdmShelfSlotPort.from_formatted_string(input_port)
    # The conversion from dict was added to take into account when the value is being deserialized
    if isinstance(input_port, dict):
        return WdmShelfSlotPort(**input_port)
    if isinstance(input_port, WdmShelfSlotPort):
        return input_port
    raise ValueError("Unknown type passed as port value must be str | WdmShelfSlotPort.")


# Used to validate values of the type NETH=89
def _validate_neth_number(neth_number_str: str) -> str:
    if neth_number_str.startswith("NETH=") and neth_number_str.split("=")[1].isdigit():
        return neth_number_str
    raise ValueError(f"Could not convert the NETH value: {neth_number_str}")


@dataclass(frozen=True)
class CsvHuaweiServiceInterfaceNeth:
    meid_id: int
    meid_name: str  # Name of the device, for e.g. PAABA-G01-1800V-01
    name_service: str  # Name of the service, for e.g. EthNatServ-PAABA-G01-171-TIS-TIS_392138
    id_service: Annotated[str, BeforeValidator(_validate_neth_number)]
    meid_node_c: str | None
    port_c: Annotated[
        WdmShelfSlotPort, BeforeValidator(_normalize_wdm_ports)
    ]  # primary shelf slot port, for e.g .shelf=0-slot=4-port=1;
    svlan: str  # list of svlans, for e.g IVID=171,358;
    meid_node_d: str | None
    port_d: str | None  # secondary shelf slot port, for e.g .shelf=0-slot=4-port=3;
    svlan_d: str  # list of translation svlans, for e.g. IVID=156,358;

    @property
    def neth_number(self) -> int:
        return int(self.id_service.split("=")[1])

    @property
    def svlans_list(self) -> list[int]:
        return self._get_all_svlans(self.svlan)

    @property
    def translation_svlans_list(self) -> list[int]:
        return self._get_all_svlans(self.svlan_d)

    @staticmethod
    def _get_all_svlans(svlan: str) -> list[int]:
        if svlan == "IVID=empty":
            return []
        svlan_values = svlan.split("=")[1]
        return list(map(int, svlan_values.split(",")))

    @staticmethod
    def _check_svlans_format(svlan_str: str) -> bool:
        if svlan_str == "IVID=empty":
            return True
        if not svlan_str.startswith("IVID="):
            return False
        try:
            values = svlan_str.split("=")[1].split(",")
            return all(v.isdigit() for v in values)
        except Exception:
            return False

    @model_validator(mode="after")
    def validate_model(self) -> "CsvHuaweiServiceInterfaceNeth":
        if not self._check_svlans_format(self.svlan):
            raise ValueError(f"Invalid svlan: {self.svlan}")
        if not self._check_svlans_format(self.svlan_d):
            raise ValueError(f"Invalid svlan_d: {self.svlan_d}")
        if len(self._get_all_svlans(self.svlan)) != len(self._get_all_svlans(self.svlan_d)):
            raise ValueError(f"Mismatch in number of SVLANs: svlan={self.svlan}, svlan_d={self.svlan_d}")
        return self
