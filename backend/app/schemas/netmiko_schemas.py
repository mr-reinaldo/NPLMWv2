from pydantic import BaseModel, Field, PositiveInt
from pydantic.networks import IPvAnyAddress
from enum import Enum
from typing import Optional


class DeviceType(str, Enum):
    cisco_ios = "cisco_ios"


class NetmikoConn(BaseModel):
    device_type: DeviceType = Field(..., description="Tipo de dispositivo")
    host: IPvAnyAddress = Field(..., description="Endereço IP do dispositivo")
    username: str = Field(..., description="Nome de usuário")
    password: str = Field(..., description="Senha")
    port: Optional[PositiveInt] = Field(22, description="Porta de conexão")
