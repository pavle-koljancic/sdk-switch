from typing import Any

import pytest

from models.db_nso.bea_preprovisioning_entity import BeaPreprovisioningEntity


class TestBeaPreprovisioningEntity:
    @pytest.mark.parametrize(
        "input",
        [
            (
                {
                    "resource_id": "ZS0106122797/1",
                    "pop_name": "AGAAB",
                    "svlan": 3928,
                    "starting_equipment": "AGAAB-G01-1830ONEHOTN10G-00",
                    "interface": "3/2/12",
                }
            ),
        ],
    )
    def test_validation_success(self, input: dict[str, Any]):
        entity = BeaPreprovisioningEntity.model_validate(input)
        assert isinstance(entity, BeaPreprovisioningEntity)

    @pytest.mark.parametrize(
        "input",
        [
            (
                {
                    "resource_id": "ZS0106122797/1",
                    "pop_name": "AGAAB",
                    "svlan": -100,
                    "starting_equipment": "AGAAB-G01-1830ONEHOTN10G-00",
                    "interface": "3/2/12",
                }
            ),
        ],
    )
    def test_validation_failed(self, input: dict[str, Any]):
        with pytest.raises(ValueError):
            BeaPreprovisioningEntity.model_validate(input)
