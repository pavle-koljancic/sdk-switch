from typing import Self

from pydantic import model_validator
from pydantic.dataclasses import dataclass


# Data model for HUAWEI_SERVICES_INTERFACES_CSV_FILE
# Represents the a service connection between 2 devices(node_a and node_b)
@dataclass(frozen=True)
class CsvHuaweiServiceInterface:
    service_name: str  # Name of the service connected
    service_id: int
    node_a: str
    # Interface on device A on which the services svlan is conncted
    port_a: str  # shelf=0-slot=11-port=3
    # Svlan on device A which the service uses
    svlan_a: str  # IVID=124 or IVID=empty 124 is the SVLAN
    node_b: str  # Interface on device B on which the services svlan is conncted
    port_b: str  # shelf=0-slot=11-port=3  or empty
    # Svlan on device A which the service uses
    svlan_b: str | None  # IVID=123 or IVID=empty

    @classmethod
    def _svlan_list_from_ivid_string(cls, ivid_str: str) -> list[int]:
        if ivid_str == "IVID=empty":
            return []
        svlan_str = ivid_str.split("=")[1]
        return list(map(int, svlan_str.split(",")))

    @property
    def svlans(self) -> list[int]:
        return CsvHuaweiServiceInterface._svlan_list_from_ivid_string(self.svlan_a)

    @property
    def translation_svlans(self) -> list[int]:
        if self.svlan_b:
            return CsvHuaweiServiceInterface._svlan_list_from_ivid_string(self.svlan_b)
        return []

    # Method used for checking that all svlan values in a list are correct:
    @classmethod
    def _check_svlans_from_ivid_string(cls, ivid_str: str) -> bool:
        svlans = ivid_str.split("=")[1].split(",")
        return all(s.isdigit() for s in svlans)

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if "IVID=" not in self.svlan_a:
            raise ValueError(f"Wrong value svlan_a:{self.svlan_a}. Should contain IVID string.")

        if self.svlan_a != "IVID=empty" and not CsvHuaweiServiceInterface._check_svlans_from_ivid_string(self.svlan_a):
            raise ValueError(f"Incorrect value for svlan_a:{self.svlan_a}")

        # for an missing svlan_b no further validation is needed
        if not self.svlan_b:
            return self

        if "IVID=" not in self.svlan_b:
            raise ValueError(f"Wrong value svlan_b:{self.svlan_b}. Should contain IVID string.")

        if self.svlan_b != "IVID=empty" and not CsvHuaweiServiceInterface._check_svlans_from_ivid_string(
            str(self.svlan_b)
        ):
            raise ValueError(f"Incorrect value for svlan_b:{self.svlan_b}")

        # If both are not empty then they should have a mtaching number of svlans
        if self.svlans and self.translation_svlans and len(self.svlans) != len(self.translation_svlans):
            raise ValueError(
                f"Mismatch in lengths for svlan_a:{len(self.svlans)} and  svlan_b:{len(self.translation_svlans)}."
            )
        return self
