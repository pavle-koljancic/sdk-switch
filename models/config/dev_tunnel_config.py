from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class DevTunnelConfig(BaseSettings):
    """
    Configuration class for Dev ssh tunneling parameters.
    Parameters are by default loaded from the environment variables otherwise None.

    Attributes:
        user: Username for connecting the host from which to tunnel.
        password (str): Password for tunnel host.
        host (str): IP address of the machine  to which we tunnel.
        port (int): Port on which we connect to the machine. The default is 22.
    """

    host: str | None = None
    user: str | None = None
    password: str | None = None
    port: int = 22

    model_config = SettingsConfigDict(
        str_min_length=1,
        extra="forbid",
        env_prefix="dev_tunnel_",
    )

    @model_validator(mode="after")
    def validate_tunnel_fields(self) -> Self:
        if self.host and self.user and self.password:
            return self  # All are set
        if self.host is None or self.user is None and self.password is None:
            return self  # All unset no tunnel configured
        raise ValueError(
            "dev_tunnel_host, dev_tunnel_user, and dev_tunnel_password must be either all None or all non-None."
        )
