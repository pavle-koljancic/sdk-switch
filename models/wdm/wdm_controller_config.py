from pydantic import BaseModel
from pydantic import ConfigDict


class BaseControllerConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str

    model_config = ConfigDict(
        extra="allow",
        str_min_length=1,
    )


class HuaweiControllerConfig(BaseControllerConfig):
    pass


class SiaeControllerConfig(BaseControllerConfig):
    pass
