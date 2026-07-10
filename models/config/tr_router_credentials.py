from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class TrRouterCredentials(BaseSettings):
    """
    Configuration class for TR Router SSH credentials info.
    Parameters must be defined.

    Attributes:
        user: Username for the TR routers.
        password (str): Password for the TR routers.
    """

    user: str
    password: str

    model_config = SettingsConfigDict(
        str_min_length=1,
        extra="forbid",
        env_prefix="tr_router_",
    )
