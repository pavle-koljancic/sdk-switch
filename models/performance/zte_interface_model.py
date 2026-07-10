from pydantic import BaseModel


class ZteInterface(BaseModel):
    type_and_port: str
    admin: str
    physical: str
    protocol: str

    def is_subinterface(self) -> bool:
        return "." in self.type_and_port
