from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class NSOConfig(BaseSettings):
    """
    Configuration class for Cisco NSO parameters. Parameters are by default
    loaded from the environment variables.

    Attributes:
        nso_user (str): The username for connecting to Cisco NSO.
        nso_password (str): The password for connecting to Cisco NSO.
        nso_host (str): IP address of the Cisco NSO server.
        nso_port (int): The port number for the Cisco NSO server. Default is 8080.
    """

    nso_user: str
    nso_password: str
    nso_host: str
    nso_host_internal: str | None = None
    nso_port: int = Field(default=8080)

    model_config = SettingsConfigDict(
        str_min_length=1,
        extra="forbid",
        env_prefix="openfb_",
    )

    def get_host(self) -> str:
        if self.nso_host_internal:
            return self.nso_host_internal
        return self.nso_host
