from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria_id: int = Field(..., gt=0) # Cambiado de id_categoria

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1)
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    categoria_id: int | None = Field(None, gt=0)

class ProductoResponse(ProductoBase):
    id: int
    class Config:
        from_attributes = True