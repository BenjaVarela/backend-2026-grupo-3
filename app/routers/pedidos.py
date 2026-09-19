from fastapi import APIRouter, HTTPException
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.repositories.pedidos_repository import PedidosRepository

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = PedidosRepository()

@router.post("/", response_model=PedidoResponse, status_code=201)
def crear_pedido(pedido: PedidoCreate):
    return repo.guardar(pedido.model_dump())

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos():
    return repo.obtener_todos()

@router.get("/{pedido_id}", response_model=PedidoResponse)
def obtener_pedido(pedido_id: int):
    pedido = repo.obtener_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.put("/{pedido_id}", response_model=PedidoResponse)
def actualizar_pedido(pedido_id: int, pedido: PedidoCreate):
    actualizado = repo.actualizar(pedido_id, pedido.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return actualizado

@router.delete("/{pedido_id}", status_code=204)
def eliminar_pedido(pedido_id: int):
    eliminado = repo.eliminar(pedido_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return