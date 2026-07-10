from enum import Enum

from pydantic import BaseModel

from models.wdm.service_nso.service_type_nso import ServiceTypeNso


class InterfaceType(Enum):
    INTERFACE_A = "interface_A"
    INTERFACE_B = "interface_B"


class WdmInterfaces(BaseModel):
    interface_a: list[str] | None = None
    interface_b: list[str] | None = None
    service: ServiceTypeNso
    active: bool = False

    def update_indexes(self, interface: InterfaceType, interface_indexes: list[str]) -> None:
        """
        Updates the interface indexes and sets the object as active.

        :param interface: The interface to update ('INTERFACE_A' or 'INTERFACE_B').
        :param interface_indexes: A list of indexes to assign to the interface.
        """
        if interface_indexes:
            self.active = True

            if interface == InterfaceType.INTERFACE_A:
                self.interface_a = interface_indexes
            elif interface == InterfaceType.INTERFACE_B:
                self.interface_b = interface_indexes
