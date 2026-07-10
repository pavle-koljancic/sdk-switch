from typing import Self

from pydantic import model_validator
from pydantic.dataclasses import dataclass


# Data model for SIAE_ALL_SERVICES_CSV_FILE
# Represents the a service connection between 2 devices(node_a and node_b)
@dataclass(frozen=True)
class CsvSiaeService:
    service_name: str  # Name of the service connected
    service_id: int
    node_a: str
    uni_node_a: str
    svlan_a: str  # 11,34,5353 or 123; Can be a list of svalns separated by a comma
    node_b: str
    uni_node_2: str
    svlan_b: str | None  # 11,34,5353 or 123 or empty ; Can be a list of svalns separated by a comma
    configuration_state: str | None
    working_state: str | None

    @property
    def svlan_list(self) -> list[int]:
        return list(map(int, self.svlan_a.split(",")))

    @property
    def svlan_translation_list(self) -> list[int]:
        # This check was added because the list can be empty
        if self.svlan_b:
            return list(map(int, self.svlan_b.split(",")))
        return []

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        svlan_list = self.svlan_list
        if not self.svlan_list:
            raise ValueError(f"svlan_a:{self.svlan_a} column in SIAE_ALL_SERVICES_CSV_FILE is empty!")
        if self.svlan_translation_list and len(svlan_list) != len(self.svlan_translation_list):
            raise ValueError(
                f"Mismatch in lengths for svlan_a:{len(svlan_list)} and  svlan_b:{len(self.svlan_translation_list)}."
            )
        return self
