from typing import Any

import pytest

from models.wdm.wdm_device import WdmDevice
from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


class TestWdmDevice:
    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because WDM device name is empty
                {
                    "name": "",
                    "shelves_slots_ports": set(WdmShelfSlotPort(shelf=0, slot=0, port=0)),
                    "primary_shelf_slot_port": WdmShelfSlotPort(shelf=0, slot=0, port=0),
                }
            )
        ],
    )
    def test_failure_empty_name(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            WdmDevice(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because Shelves_slot_ports is empty
                {
                    "name": "PAABA-G01-1800V-01",
                    "shelves_slots_ports": set(),
                    "primary_shelf_slot_port": WdmShelfSlotPort(shelf=0, slot=0, port=0),
                }
            )
        ],
    )
    def test_failure_empty_shelves_slot_port(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            WdmDevice(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because primary_shelf_slot_port is not a member of shelves_slots_ports
                {
                    "name": "PAABA-G01-1800V-01",
                    "shelves_slots_ports": set(WdmShelfSlotPort(shelf=0, slot=0, port=0)),
                    "primary_shelf_slot_port": WdmShelfSlotPort(shelf=1, slot=0, port=0),
                }
            )
        ],
    )
    def test_failure_unknown_vendor(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            WdmDevice(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because vendor cannot be determined from name
                {
                    "name": "FAKE_NAME",
                    "shelves_slots_ports": set(WdmShelfSlotPort(shelf=0, slot=0, port=0)),
                    "primary_shelf_slot_port": WdmShelfSlotPort(shelf=1, slot=0, port=0),
                }
            )
        ],
    )
    def test_failure_primary_not_member(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            WdmDevice(**input)

    @pytest.mark.parametrize(
        "input",
        [
            # SIAE
            ("FGANA-G01-1830ONEHOTN10G-00 1/4/3 1/4/3"),
            # Huawei
            ("PAABA-G01-1800V-01 4/3 4/3"),
            # Huawei with leading 0
            ("PAABA-G01-1800V-01 0/4/3 0/4/3"),
            # Huawei with leading /
            ("PAABA-G01-1800V-01 /4/3 /4/3"),
        ],
    )
    def test_success_from_string(self, input: str):
        WdmDevice.from_path_str(input)

    @pytest.mark.parametrize(
        "input",
        [
            # SIAE CANNOT start with a /
            ("FGANA-G01-1830ONEHOTN10G-00 /4/3 /4/3")
        ],
    )
    def test_failure_from_string(self, input: str):
        with pytest.raises(ValueError):
            WdmDevice.from_path_str(input)
