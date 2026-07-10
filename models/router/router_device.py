# Model used for representing a service configuration on a sub interface
from typing import Annotated
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import StringConstraints

from models.router.router_os_version import CiscoOSVersion


class BaseConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    neighbor_pw_id: str
    evpn_id: str | None = None  # This was done because evpn id doesn't exist currently for CISCO IOS devices


class XConnectConfig(BaseConfig):
    type: Literal["xconnect"]
    xconnect_group_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    p2p_name: str


class BridgeConfig(BaseConfig):
    type: Literal["bridge"]
    bridge_domain_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    bridge_group: str | None = None
    vfi_name: str


SubInterfaceServiceConfig = Annotated[
    XConnectConfig | BridgeConfig,
    Field(discriminator="type"),
]


class RouterConfiguration(BaseModel):
    model_config = ConfigDict(frozen=True)
    device_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    interface_type: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    interface_number: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    device_os: CiscoOSVersion
    svlan: int
    config: SubInterfaceServiceConfig | None
