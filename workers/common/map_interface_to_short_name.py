from conductor.client import worker_task
from conductor.client.http.models.task_def import TaskDef

from models.router.router_interfaces import CiscoIOSInterface
from models.router.router_interfaces import CiscoIOSXrInterface


def _full_to_short_interface(full_name: str, os_version: str) -> str | None:
    """Convert full interface name to short enum key"""
    enum_cls = CiscoIOSInterface if os_version == "cisco-ios" else CiscoIOSXrInterface
    for key in enum_cls:
        if key.value == full_name:
            return key.name
    return None


@worker_task(
    task_definition_name="map_interface_to_short_name",
    register_task_def=True,  # Auto-register on startup
    task_def=TaskDef(
        description=("Convert full interface name to short enum key (Te/Ge/Hu)"),
        timeout_seconds=60,
        response_timeout_seconds=60.0,
    ),
)
def map_interface_to_short_name(interface_full: str, os_version: str) -> str:
    short_ifc = _full_to_short_interface(interface_full, os_version)
    if short_ifc is None:
        raise ValueError(f"Could not map '{interface_full}' to a short interface key for OS '{os_version}'")

    short_interface = short_ifc
    return short_interface
