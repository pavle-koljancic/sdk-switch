from pydantic import BaseModel


class TrailRingResult(BaseModel):
    nome_wdm_3: str
    ifc_wdm_3: str
    nome_wdm_4: str
    ifc_wdm_4: str
    router_pe1: str
    ifc_router_pe1: str
