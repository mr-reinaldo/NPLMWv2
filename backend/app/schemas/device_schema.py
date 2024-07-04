from pydantic import BaseModel, Field, PositiveInt, ConfigDict, field_validator
from pydantic.networks import IPvAnyAddress
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from re import match


class BaseSchema(BaseModel):
    model_config: ConfigDict = ConfigDict({"from_attributes": True})


class DeviceSchema(BaseSchema):
    ip_address: IPvAnyAddress = Field(
        ..., description="Endereço IP do dispositivo"
    )
    hostname: Optional[str] = Field(None, description="Nome do host")
    username: str = Field(..., description="Nome de usuário")
    password: str = Field(..., description="Senha do dispositivo")
    driver_name: str = Field(..., description="Nome do driver")
    device_type: str = Field(..., description="Tipo do dispositivo")
    port_number: PositiveInt = Field(
        22, description="Número da porta do dispositivo"
    )
    description: Optional[str] = Field(
        None, description="Descrição do dispositivo"
    )

    # @field_validator("ip_address")
    # def ip_address_validator(cls, v):
    #     if not match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", v):
    #         raise ValueError("Endereço IP inválido")
    #     return v

    @field_validator("port_number")
    def port_number_validator(cls, v):
        if v < 1 or v > 65535:
            raise ValueError("Número de porta inválido")
        return v


class DeviceSchemaPublic(BaseSchema):
    id: UUID = Field(..., description="ID do dispositivo")
    user_id: UUID = Field(..., description="ID do usuário")
    ip_address: IPvAnyAddress = Field(
        ..., description="Endereço IP do dispositivo"
    )
    hostname: Optional[str] = Field(None, description="Nome do host")
    username: str = Field(..., description="Nome de usuário")
    driver_name: str = Field(..., description="Nome do driver")
    device_type: str = Field(..., description="Tipo do dispositivo")
    port_number: PositiveInt = Field(
        ..., description="Número da porta do dispositivo"
    )
    description: Optional[str] = Field(
        None, description="Descrição do dispositivo"
    )
    created_at: datetime = Field(
        ..., description="Data de criação do dispositivo"
    )
    updated_at: datetime = Field(
        ..., description="Data de atualização do dispositivo"
    )


class DeviceSchemaUpdate(BaseSchema):
    ip_address: Optional[IPvAnyAddress] = Field(
        None, description="Endereço IP do dispositivo"
    )
    hostname: Optional[str] = Field(None, description="Nome do host")
    username: Optional[str] = Field(None, description="Nome de usuário")
    password: Optional[str] = Field(None, description="Senha do dispositivo")
    driver_name: Optional[str] = Field(None, description="Nome do driver")
    device_type: Optional[str] = Field(None, description="Tipo do dispositivo")
    port_number: Optional[PositiveInt] = Field(
        None, description="Número da porta do dispositivo"
    )
    description: Optional[str] = Field(
        None, description="Descrição do dispositivo"
    )

    # @field_validator("ip_address")
    # def ip_address_validator(cls, v):
    #     if not match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", v):
    #         raise ValueError("Endereço IP inválido")
    #     return v

    @field_validator("port_number")
    def port_number_validator(cls, v):
        if v < 1 or v > 65535:
            raise ValueError("Número de porta inválido")
        return v


class DeviceSchemaList(BaseSchema):
    devices: List[DeviceSchemaPublic] = Field(
        ..., description="Lista de dispositivos"
    )
