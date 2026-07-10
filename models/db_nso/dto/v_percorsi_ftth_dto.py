from typing import Annotated
from typing import Self

from pydantic import ConfigDict
from pydantic import StringConstraints
from pydantic import model_serializer
from pydantic import model_validator

from models.db_nso.v_percorsi_ftth import VPercorsiFtthEntity


class VPercorsiFtthDTO(VPercorsiFtthEntity):
    model_config = ConfigDict(frozen=True)

    nome_olt: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    pop: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    nome_wdm_0: str | None = None

    ifc_wdm_0: str | None = None

    ifc_wdm_0_delivery: str | None = None

    nome_wdm_1: str | None = None

    ifc_wdm_1: str | None = None

    nome_wdm_2: str | None = None

    ifc_wdm_2: str | None = None

    nome_wdm_3: str | None = None

    ifc_wdm_3: str | None = None

    nome_wdm_4: str | None = None

    ifc_wdm_4: str | None = None

    router_pe1: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    ifc_router_type: str | None = None

    ifc_router_pe1: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    def _is_not_empty(self, value: str | None) -> bool:
        return value is not None and value.strip() != ""

    def is_layer3_valid(self) -> bool:
        return all(
            [
                self._is_not_empty(self.nome_wdm_0),
                self._is_not_empty(self.ifc_wdm_0),
                self._is_not_empty(self.ifc_wdm_0_delivery),
            ]
        )

    def is_chain_valid(self) -> bool:
        return all(
            [
                self._is_not_empty(self.nome_wdm_1),
                self._is_not_empty(self.ifc_wdm_1),
                self._is_not_empty(self.nome_wdm_2),
                self._is_not_empty(self.ifc_wdm_2),
            ]
        )

    def is_ring_valid(self) -> bool:
        return all(
            [
                self._is_not_empty(self.nome_wdm_3),
                self._is_not_empty(self.ifc_wdm_3),
                self._is_not_empty(self.nome_wdm_4),
                self._is_not_empty(self.ifc_wdm_4),
            ]
        )

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if self.is_layer3_valid() or self.is_chain_valid() or self.is_ring_valid():
            return self

        raise ValueError("At least one pair of paths must be fully populated")

    @model_serializer(mode="plain")
    def serialize_model(self) -> dict[str, object]:
        return {k: getattr(self, k) for k in self.__class__.__annotations__}
