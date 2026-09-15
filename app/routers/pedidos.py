from fastapi import APIRouter
from app.schemas.pedido import Pedido
from app.services.pedido_service import crear_nuevo_pedido, obtener_pedidos

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=Pedido, status_code=201)
def crear_pedido(pedido: Pedido):
    return crear_nuevo_pedido(pedido)

@router.get("/", response_model=list[Pedido])
def listar_pedidos():
    return obtener_pedidos()