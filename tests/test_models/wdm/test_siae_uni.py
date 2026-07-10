from typing import Any

import pytest

from models.wdm.csv_models.siae_uni import CsvSiaeUni


class TestCsvSiaeUni:
    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of equipment_name is None
                {
                    "equipment_name": None,
                    "unipkt_port": "UNIPKT-GBE1-3-2-12",
                    "uni_interface_name": "test",
                    "interface_type": "test",
                }
            ),
            (  # Fails because of unipkt_port is None
                {
                    "equipment_name": "test",
                    "unipkt_port": None,
                    "uni_interface_name": "UNIPKT-GBE1-3-2-12",
                    "interface_type": "test",
                }
            ),
            (  # Fails because of uni_interface_name is None
                {"equipment_name": "test", "unipkt_port": "test", "uni_interface_name": None, "interface_type": "test"}
            ),
            (  # Fails because of interface_type is None
                {
                    "equipment_name": "test",
                    "unipkt_port": "test",
                    "uni_interface_name": "UNIPKT-GBE1-3-2-12",
                    "interface_type": None,
                }
            ),
        ],
    )
    def test_validation_failure_none_values(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            CsvSiaeUni(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of number of wdm shelf slot port not divisible by 3
                {
                    "equipment_name": "test",
                    "unipkt_port": "test",
                    "uni_interface_name": "UNIPKT-GBE-1-3-2-12",
                    "interface_type": "test",
                }
            ),
            (  # Fails because of number of wdm shelf slot port not divisible by 3
                {
                    "equipment_name": "test",
                    "unipkt_port": "test",
                    "uni_interface_name": "UNIPKT-GBE-1-3",
                    "interface_type": "test",
                }
            ),
            (  # Wrong separator
                {
                    "equipment_name": "test",
                    "unipkt_port": "test",
                    "uni_interface_name": "UNIPKT-GBE-3/2/12",
                    "interface_type": "test",
                }
            ),
            (  # Missing shelf slot port values
                {
                    "equipment_name": "test",
                    "unipkt_port": "test",
                    "uni_interface_name": "UNIPKT-GBE",
                    "interface_type": "test",
                }
            ),
        ],
    )
    def test_validation_failure_incorrect_unipkt_port(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            CsvSiaeUni(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (
                {
                    "equipment_name": "name",
                    "unipkt_port": "UNIPKT-GBE-1-3-2",
                    "uni_interface_name": "name",
                    "interface_type": "type",
                }
            )
        ],
    )
    def test_success(self, input: dict[str, Any]):
        CsvSiaeUni(**input)
