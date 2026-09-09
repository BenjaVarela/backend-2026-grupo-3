from pydantic import BaseModel, Field

class CategoriaProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre de la categoría")
    descripcion: str = Field(..., min_length=1, description="Descripción corta")
    activa: bool = True

class CategoriaProductoCreate(CategoriaProductoBase):
    pass

class CategoriaProductoResponse(CategoriaProductoBase):
    id: int

    class Config:
        from_attributes = True