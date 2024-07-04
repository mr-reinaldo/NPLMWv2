from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import List, Optional
from uuid import UUID
from re import match
from datetime import datetime

from app.schemas.device_schema import DeviceSchemaPublic


class BaseSchema(BaseModel):
    model_config: ConfigDict = ConfigDict({"from_attributes": True})


class UserSchema(BaseSchema):
    username: str = Field(
        ..., min_length=3, max_length=50, description="Nome de usuário"
    )
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")
    is_active: Optional[bool] = Field(
        True, description="Usuário ativo ou inativo"
    )

    @field_validator("username")
    def username_validator(cls, v):
        if not match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Nome de usuário inválido")
        return v

    @field_validator("password")
    def password_validator(cls, v):
        if not match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", v):
            raise ValueError(
                "Senha inválida. A senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número."
            )
        return v


class UserSchemaPublic(BaseSchema):
    id: UUID = Field(..., description="ID do usuário")
    username: str = Field(..., description="Nome de usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    is_active: bool = Field(..., description="Usuário ativo ou inativo")
    created_at: datetime = Field(..., description="Data de criação do usuário")
    updated_at: datetime = Field(
        ..., description="Data de atualização do usuário"
    )


class UserSchemaUpdate(BaseSchema):
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Nome de usuário"
    )
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    password: Optional[str] = Field(
        None, min_length=8, description="Senha do usuário"
    )
    is_active: Optional[bool] = Field(
        None, description="Usuário ativo ou inativo"
    )

    @field_validator("username")
    def username_validator(cls, v):
        if not match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Nome de usuário inválido")
        return v

    @field_validator("password")
    def password_validator(cls, v):
        if not match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", v):
            raise ValueError(
                "Senha inválida. A senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número."
            )
        return v


class UserSchemaList(BaseSchema):
    users: List[UserSchemaPublic] = Field(..., description="Lista de usuários")


class UserSchemaDevices(UserSchemaPublic):
    devices: Optional[List[DeviceSchemaPublic]] = Field(
        ..., description="Lista de dispositivos do usuário"
    )
