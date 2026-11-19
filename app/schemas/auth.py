from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

from app.domain.auth import PASSWORD_MAX, PASSWORD_MIN, Rol


Email = Annotated[EmailStr, Field(max_length=254)]
Password = Annotated[SecretStr, Field(min_length=PASSWORD_MIN, max_length=PASSWORD_MAX)]


class Identificador(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: Email


class Registro(Identificador):
    password: Password


class Login(Identificador):
    password: Annotated[SecretStr, Field(min_length=1, max_length=PASSWORD_MAX)]


class Restablecimiento(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: Annotated[SecretStr, Field(min_length=1, max_length=2048)]
    nueva_password: Password


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    rol: Rol


class AccessResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int


class Mensaje(BaseModel):
    mensaje: str
