from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class EstadoPedido(str, Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    entregado = "entregado"
    cancelado = "cancelado"

class PedidoBase(BaseModel):
    cliente_id: int = Field(..., gt=0, description="ID del cliente debe ser mayor a 0")
    producto_id: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0, le=100, description="La cantidad debe ser entre 1 y 100")
    estado: EstadoPedido = Field(default=EstadoPedido.pendiente)

class PedidoCreate(PedidoBase):
    model_config = {
        "json_schema_extra": {
            "example": {"cliente_id": 1, "producto_id": 1, "cantidad": 2}
        }
    }

class PedidoResponse(PedidoBase):
    id: int
    monto_total: float
    class Config:
        from_attributes = True