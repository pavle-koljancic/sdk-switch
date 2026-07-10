from typing import Self

from pydantic import model_validator
from pydantic.dataclasses import dataclass

from models.wdm.wdm_device import WdmDevice
from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


@dataclass(frozen=True)
class CsvHuaweiServiceInterfaceVPLS:
    service_id: int
    service_name: str  # Name of the service connected
    wdm_node: str  # devices
    svlan: str  # e.g. "IVID=456,168"
    port: str  # shelf-slot-port, e.g. shelf-0-slot=9-port=1, order of ports must match the order of devices in wdm_node
    vsi_id: str  # Antonello has said this is not relevant for us

    @staticmethod
    def _get_all_svlans(svlan: str) -> list[int]:
        svlan_values = svlan.split("=")[1]
        return list(map(int, svlan_values.split(",")))

    @property
    def svlans(self) -> list[int]:
        return self._get_all_svlans(self.svlan)

    @property
    def wdm_devices_list(self) -> list[WdmDevice]:
        """
        Convert wdm_node + ports into a list of WdmDevice objects
        where each device gets its corresponding WdmShelfSlotPort objects.
        Assumes order of devices matches order of ports  because Antonello has said that the order needs to match always.
        """
        devices = [device.strip() for device in self.wdm_node.split(",") if device.strip()]
        ports = [port.strip() for port in self.port.split(",") if port.strip()]

        if len(devices) != len(ports):
            raise ValueError(f"Number of devices ({len(devices)}) does not match number of ports ({len(ports)})")

        wdm_devices_list: list[WdmDevice] = []
        for device_name, port_str in zip(devices, ports):
            shelf_slot_port_obj = WdmShelfSlotPort.from_formatted_string(port_str)
            wdm_device = WdmDevice(
                name=device_name, shelves_slots_ports={shelf_slot_port_obj}, primary_shelf_slot_port=shelf_slot_port_obj
            )

            wdm_devices_list.append(wdm_device)

        return wdm_devices_list

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if "IVID=" not in self.svlan:
            raise ValueError(f"Wrong value. Should contain IVID string: {self.svlan}")

        svlans = self.svlan.split("=")[1].split(",")

        if not svlans or all(not v.isdigit() for v in svlans):
            raise ValueError(f"Incorrect value for svlans: {self.svlan}")

        devices = [device.strip() for device in self.wdm_node.split(",") if device.strip()]
        ports = [port.strip() for port in self.port.split(",") if port.strip()]

        if len(devices) != len(ports):
            raise ValueError(f"Number of devices ({len(devices)}) does not match number of ports ({len(ports)})")

        for device_name, port_str in zip(devices, ports):
            try:
                WdmDevice(
                    name=device_name,
                    shelves_slots_ports={WdmShelfSlotPort.from_formatted_string(port_str)},
                    primary_shelf_slot_port=WdmShelfSlotPort.from_formatted_string(port_str),
                )
            except Exception as e:
                raise ValueError(f"Invalid conversion to WdmDevice for '{device_name}' with port '{port_str}': {e}")

        return self
