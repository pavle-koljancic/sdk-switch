from typing import ClassVar

from pydantic import ConfigDict

from models.db_nso.db_base_entity import DbBaseEntity


class VPercorsiFtthEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    nome_olt: str | None = None
    ifc_olt: str | None = None

    nome_wdm_0: str | None = None
    ifc_wdm_0: str | None = None
    ifc_wdm_0_delivery: str | None = None

    pop: str | None = None

    ifc_wdm_1: str | None = None
    nome_wdm_1: str | None = None

    nome_wdm_2: str | None = None
    ifc_wdm_2: str | None = None

    nome_chain: str | None = None
    nome_pop_edge: str | None = None
    nome_pop_hub: str | None = None

    nome_ring: str | None = None

    nome_wdm_3: str | None = None
    ifc_wdm_3: str | None = None

    nome_wdm_4: str | None = None
    ifc_wdm_4: str | None = None

    tipo: str | None = None
    svlan_operator: str | None = None

    router_pe1: str | None = None
    ifc_router_pe1: str | None = None
    ifc_router_type: str | None = None
    ifc_logic_router_pe1: str | None = None

    status: str | None = None
    layer: str | None = None

    table_name: ClassVar[str] = "nso.v_percorsi_ftth"
