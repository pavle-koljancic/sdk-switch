from pydantic import BaseModel


class WDMDiscoveryOutput(BaseModel):
    svlan: int | list[int]
    id_service: int | None
    name_service: str
