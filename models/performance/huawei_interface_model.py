from pydantic import BaseModel


class HuaweiInterface(BaseModel):
    type: str
    port: str
    physical: str
    protocol: str
