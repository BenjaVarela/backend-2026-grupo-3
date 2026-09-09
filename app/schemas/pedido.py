from enum import Enum
from pydantic import BaseModel, Field

class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"

class PedidoCreate(BaseModel):
    id_cliente: int = Field(..., gt=0)
    id_producto: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")

class PedidoResponse(BaseModel):
    id: int
    id_cliente: int
    id_producto: int
    cantidad: int
    monto_total: float = Field(..., ge=0)
    estado: EstadoPedido

    class Config:
        from_attributes = True