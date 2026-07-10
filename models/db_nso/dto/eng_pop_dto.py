from typing import Annotated

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import model_serializer

from models.db_nso.db_base_entity import _validate_pop_collect
from models.db_nso.eng_pop_entity import EngPopEntity


class EngPopDTO(EngPopEntity):
    model_config = ConfigDict(frozen=True)
    pop_collect: Annotated[str, BeforeValidator(_validate_pop_collect)]

    @model_serializer(mode="plain")
    def serialize_model(self) -> dict[str, object]:
        return {"pop_collect": self.pop_collect}
