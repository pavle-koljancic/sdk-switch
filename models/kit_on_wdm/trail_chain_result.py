from pydantic import BaseModel


class TrailChainResult(BaseModel):
    ifc_wdm_1: str
    nome_wdm_1: str
    nome_wdm_2: str
    ifc_wdm_2: str
