from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class AcceadianConfig(BaseSettings):
    """
    Configuration class for Acceadian login parameters.
    Parameters are loaded from environment variables by default.
    """

    acceadian_user: str
    acceadian_password: str
    acceadian_host: str
    acceadian_port: int = Field(default=443)

    model_config = SettingsConfigDict(
        str_min_length=1,
        extra="forbid",
        env_prefix="openfb_",
    )

    def to_uri(self) -> str:
        return f"http://{self.acceadian_host}:{self.acceadian_port}/nbapiemswsweb/"
