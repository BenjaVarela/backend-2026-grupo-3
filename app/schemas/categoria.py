from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
    estado_activo: Optional[bool] = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

CategoriaProductoBase = CategoriaBase
CategoriaProductoCreate = CategoriaCreate
CategoriaProductoResponse = CategoriaResponse