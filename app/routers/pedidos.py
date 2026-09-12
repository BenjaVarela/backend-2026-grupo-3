from fastapi import APIRouter
from app.repositories.pedidos_repository import PedidosRepository
from app.schemas.pedido import PedidoCreate

router = APIRouter()
repo = PedidosRepository()

@router.get("")
def listar_pedidos():
    return repo.obtener_todos()

@router.post("", status_code=201)
def crear_pedido(pedido: PedidoCreate):
    return repo.guardar(pedido.model_dump())