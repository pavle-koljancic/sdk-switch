from typing import Annotated

from pydantic import ConfigDict
from pydantic import StringConstraints
from pydantic import model_serializer

from models.db_nso.eng_bh_cables import EngBhCablesEntity


class EngBhCablesDTO(EngBhCablesEntity):
    model_config = ConfigDict(frozen=True)

    pop: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    olt_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    nome_wdm_1: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    ifc_wdm_1_collect: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    ifc_wdm_1_delivery: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    router_pe1: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    ifc_router_type: str | None = None

    ifc_router_pe1: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    @model_serializer(mode="plain")
    def serialize_model(self) -> dict[str, object]:
        return {k: getattr(self, k) for k in self.__class__.__annotations__}
