from typing import Any

from pydantic import BaseModel
from pydantic import field_validator
from pydantic_settings import SettingsConfigDict


class Svlan(BaseModel):
    olo: str
    svlan: int
    svlan_translation_olo: int | None
    cos: str | None
    kit: str
    resource_id: str
    mode: str
    auth: str | None

    model_config = SettingsConfigDict(
        extra="allow",
    )

    @field_validator("svlan_translation_olo", mode="before")
    def validate_empty_to_none(cls, v: Any) -> Any:
        return None if isinstance(v, str) and not v else v

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Svlan):
            return self.svlan == other.svlan
        return False

    def __hash__(self) -> int:
        return hash(self.svlan)
