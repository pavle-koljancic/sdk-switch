from datetime import datetime
from typing import Any

import pytest

from models.db_nso.db_base_entity import _validate_svlan
from models.db_nso.db_base_entity import convert_str_to_datetime


class TestDbEntityValidators:
    @pytest.mark.parametrize(
        "input",
        [(1117), ("3908"), (None), (0)],
    )
    def test_svlan_validation_success(self, input: Any):
        result = _validate_svlan(input)
        assert result is None or isinstance(result, int)

    @pytest.mark.parametrize(
        "input",
        [
            (-1117),
            ("-3908"),
            ("0.1"),
            (0.1),
            (-1),
        ],
    )
    def test_svlan_validation_failure(self, input: Any):
        with pytest.raises(ValueError):
            _validate_svlan(input)

    @pytest.mark.parametrize(
        "input",
        [
            ("2024-03-28 14:41:36.480301"),
            ("2024-10-19 19:04:10.779684"),
            (None),
            (datetime.strptime("2025-04-02 16:48:33.262894", "%Y-%m-%d %H:%M:%S.%f")),
        ],
    )
    def test_datetime_validation_success(self, input: Any):
        result = convert_str_to_datetime(input)
        assert result is None or isinstance(result, datetime)

    @pytest.mark.parametrize(
        "input",
        [("-2024-03-28 14:41:36.480301"), ("2024-19 19:04:10.779684"), ("20 14:41:36.480301"), ("2024-779684")],
    )
    def test_datetime_validation_failed(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            convert_str_to_datetime(input)
