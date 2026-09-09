from pydantic import BaseModel, EmailStr, Field

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del cliente")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    telefono: str = Field(..., min_length=8, description="Teléfono de contacto")
    tipo_cliente: str = Field(..., min_length=1, description="Estudiante o Docente")

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True