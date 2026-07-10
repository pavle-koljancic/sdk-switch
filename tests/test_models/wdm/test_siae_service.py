from typing import Any

import pytest

from models.wdm.csv_models.siae_service import CsvSiaeService


class TestCsvSiaeService:
    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of service_name is None
                {
                    "service_name": None,
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of service_id is None
                {
                    "service_name": "test",
                    "service_id": None,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of node_a is None
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": None,
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of uni_node_a is None
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": None,
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of svlan_a is None
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": None,
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of node_b is None
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": None,
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of uni_node_2 is None
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": None,
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
        ],
    )
    def test_validation_failure_none_values(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            CsvSiaeService(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (  # Fails because of service_id cannot be converted to int
                {
                    "service_name": "test",
                    "service_id": "b",
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (  # Fails because of mismatch in length of svlan and svlan_translation
                {
                    "service_name": "test",
                    "service_id": "2",
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1,23",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": "4",
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
        ],
    )
    def test_validation_failure_incorrect_values(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            CsvSiaeService(**input)

    @pytest.mark.parametrize(
        "input",
        [
            (
                {
                    "service_name": "test",
                    "service_id": "1",
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1,2,3",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": "4,5,6",
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
            (
                {
                    "service_name": "test",
                    "service_id": 1,
                    "node_a": "test",
                    "uni_node_a": "test",
                    "svlan_a": "1,2,3",
                    "node_b": "test",
                    "uni_node_2": "test",
                    "svlan_b": None,
                    "configuration_state": None,
                    "working_state": None,
                }
            ),
        ],
    )
    def test_validation_succes(self, input: dict[str, Any]):
        CsvSiaeService(**input)
