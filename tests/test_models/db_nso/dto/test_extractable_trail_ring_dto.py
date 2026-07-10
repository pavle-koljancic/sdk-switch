from typing import Any

import pytest
from pydantic import ValidationError

from models.db_nso.dto.extractable_trail_ring import ExtractableTrailRingDTO


class TestExtractableTrailRingDTO:
    @pytest.mark.parametrize(
        "input_data",
        [
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/3",
                "ifc_router_pe1": "1/2/3",
            },
        ],
    )
    def test_validation_success(self, input_data: dict[str, Any]):
        entity = ExtractableTrailRingDTO.model_validate(input_data)

        assert isinstance(entity, ExtractableTrailRingDTO)
        assert entity.nome_wdm_3 == input_data["nome_wdm_3"]
        assert entity.nome_wdm_4 == input_data["nome_wdm_4"]
        assert entity.router_pe1 == input_data["router_pe1"]
        assert entity.ifc_wdm_3 == input_data["ifc_wdm_3"]
        assert entity.ifc_wdm_4 == input_data["ifc_wdm_4"]
        assert entity.ifc_router_pe1 == input_data["ifc_router_pe1"]

    @pytest.mark.parametrize(
        "input_data",
        [
            # nome_wdm_3=None
            {
                "nome_wdm_3": None,
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": "1/2/3",
            },
            # nome_wdm_4=None
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": None,
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": "1/2/3",
            },
            # router_pe1=None
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": None,
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": "1/2/3",
            },
            # ifc_wdm_3=None
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": None,
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": "1/2/3",
            },
            # ifc_wdm_4=None
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": None,
                "ifc_router_pe1": "1/2/3",
            },
            # ifc_router_pe1=None
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": None,
            },
            # invalid ifc_wdm_3
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "pp1/2/3",
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": "1/2/3",
            },
            # invalid ifc_wdm_3
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "3",
                "ifc_wdm_4": "1/2",
                "ifc_router_pe1": "1/2/3",
            },
            # invalid ifc_wdm_4
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/-3",
                "ifc_router_pe1": "1/2/3",
            },
            # invalid ifc_wdm_4
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "1/p2/3",
                "ifc_router_pe1": "1/2/3",
            },
        ],
    )
    def test_validation_failed(self, input_data: dict[str, Any]):
        with pytest.raises((ValidationError, ValueError)):
            ExtractableTrailRingDTO.model_validate(input_data)

    @pytest.mark.parametrize(
        "input_data",
        [
            {
                "nome_wdm_3": "nome_3",
                "nome_wdm_4": "nome_4",
                "router_pe1": "router_p1",
                "ifc_wdm_3": "1/2",
                "ifc_wdm_4": "3/4",
                "ifc_router_pe1": "1/2/3",
            },
        ],
    )
    def test_port_properties(self, input_data: dict[str, Any]):
        entity = ExtractableTrailRingDTO.model_validate(input_data)

        assert entity.ifc_3__shelf_slot_port == entity.ifc_3__shelf_slot_port
        assert entity.ifc_4__shelf_slot_port == entity.ifc_4__shelf_slot_port
