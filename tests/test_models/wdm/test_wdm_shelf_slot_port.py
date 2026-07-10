from typing import Any

import pytest

from models.wdm.wdm_shelf_slot_port import WdmShelfSlotPort


class TestWdmShelfPort:
    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of negative value for slot
                {
                    "shelf": "8",
                    "slot": -1,
                    "port": 3,
                }
            ),
            (  # Fails because slot is not non negative int
                {
                    "shelf": "8",
                    "slot": "3p",
                    "port": 3,
                }
            ),
            (  # Fails because of negative value for port
                {
                    "shelf": "8",
                    "slot": 1,
                    "port": -3,
                }
            ),
            (  # Fails because port is not non negative int
                {
                    "shelf": "8",
                    "slot": 1,
                    "port": "p3",
                }
            ),
        ],
    )
    def test_dict_validation_failure_port_or_slot(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            WdmShelfSlotPort(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of double 'a' in shelf
                {
                    "shelf": "a8",
                    "slot": "1",
                    "port": 2,
                }
            ),
            (  # Fails because of double 'pp' in shelf
                {
                    "shelf": "pp8",
                    "slot": "1",
                    "port": 2,
                }
            ),
            (  # Fails because of negative value for shelf
                {
                    "shelf": "-8",
                    "slot": 2,
                    "port": 3,
                }
            ),
        ],
    )
    def test_dict_validation_failure_shelf(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            WdmShelfSlotPort(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of double p in slot position
                "p8/1"
            ),
            (  # Fails because of negative number
                "-8/2/3"
            ),
            (  # Fails because of negative number
                "8/-1/3"
            ),
            (  # Fails to many values
                "1/2/3/4"
            ),
            (  # Fails to few values
                "/4"
            ),
            (  # Fails empty string
                ""
            ),
        ],
    )
    def test_validation_str_failure(self, input: str):
        with pytest.raises(ValueError):
            WdmShelfSlotPort.from_str(input)

    @pytest.mark.parametrize(
        "input",
        [
            ("8/1"),
            ("p8/2/3"),
            ("1/2/3"),
        ],
    )
    def test_validation_str_success(self, input: str):
        shelf_slot_port = WdmShelfSlotPort.from_str(input)
        split_input = input.split("/")
        if len(split_input) == WdmShelfSlotPort.num_of_ports_full:
            assert (
                split_input[0] == shelf_slot_port.shelf
                and split_input[1] == shelf_slot_port.slot
                and split_input[2] == shelf_slot_port.port
            )
        elif len(split_input) == WdmShelfSlotPort.num_of_ports_short:
            assert (
                "0" == shelf_slot_port.shelf
                and split_input[0] == shelf_slot_port.slot
                and split_input[1] == shelf_slot_port.port
            )
        else:
            raise ValueError("Improper length or format of input string")

    @pytest.mark.parametrize(
        "input",
        [
            (
                {
                    "shelf": 1,
                    "slot": 3,
                    "port": 3,
                }
            ),
            (
                {
                    "shelf": "8",
                    "slot": 1,
                    "port": 3,
                }
            ),
            (
                {
                    "extra_1": "SOMETHING",
                    "shelf": "p8",
                    "slot": 1,
                    "port": "3",
                    "extra_2": "SOMETHING",
                }
            ),
        ],
    )
    def test_validation_dict_success(self, input: dict[str, Any]):
        shelf_slot_port = WdmShelfSlotPort(**input)
        assert (
            str(input["shelf"]) == shelf_slot_port.shelf
            and str(input["slot"]) == shelf_slot_port.slot
            and str(input["port"]) == shelf_slot_port.port
        )
