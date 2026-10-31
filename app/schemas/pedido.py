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
    monto_total: float = Field(..., gt=0)
    estado: EstadoPedido = Field(default=EstadoPedido.pendiente)

class PedidoCreate(PedidoBase):
    pass

class PedidoResponse(PedidoBase):
    id: int

    class Config:
        from_attributes = True