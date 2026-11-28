from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria_id: int = Field(..., gt=0)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1)
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    categoria_id: int | None = Field(None, gt=0)

class ProductoResponse(ProductoBase):
    categoria_id: int | None = None
    id: int
    class Config:
        from_attributes = True

class ProductoPagina(BaseModel):
    items: list[ProductoResponse]
    total: int
    pagina: int
    limite: int
    total_paginas: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [{"id": 3, "nombre": "Café americano", "precio": 1200.0, "stock": 20, "categoria_id": 1}],
                "total": 3,
                "pagina": 1,
                "limite": 1,
                "total_paginas": 3,
            }
        }
    }