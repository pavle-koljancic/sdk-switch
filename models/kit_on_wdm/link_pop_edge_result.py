from pydantic import BaseModel


class LinkPopEdgeResult(BaseModel):
    nome_wdm_2: str
    ifc_wdm_2: str
    nome_wdm_3: str
    ifc_wdm_3: str
