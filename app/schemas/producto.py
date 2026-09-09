from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="El precio debe ser positivo")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    id_categoria: int = Field(..., gt=0, description="ID de la categoría asociada")

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1)
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    id_categoria: int | None = Field(None, gt=0)

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True