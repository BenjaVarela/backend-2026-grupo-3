from enum import Enum
from pydantic import BaseModel, Field

class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"

class PedidoCreate(BaseModel):
    cliente_id: int = Field(..., gt=0)   # Cambiado
    producto_id: int = Field(..., gt=0)  # Cambiado
    cantidad: int = Field(..., gt=0)

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    producto_id: int
    cantidad: int
    monto_total: float = Field(..., ge=0)
    estado: EstadoPedido
    class Config:
        from_attributes = True