from fastapi import APIRouter, HTTPException, Query
from app.schemas.pedido import PedidoCreate, PedidoResponse, EstadoPedido
from app.services.pedido_service import crear_pedido_servicio
from app.repositories.pedidos_repository import PedidosRepository

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = PedidosRepository()

@router.post("/", response_model=PedidoResponse, status_code=201)
def crear_pedido(pedido: PedidoCreate):
    return crear_pedido_servicio(pedido)

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(estado: EstadoPedido | None = Query(None, description="Filtrar pedidos por estado")):
    pedidos = repo.obtener_todos()
    if estado:
        pedidos = [p for p in pedidos if p["estado"] == estado.value or p["estado"] == estado]
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoResponse)
def obtener_pedido(pedido_id: int):
    pedido = repo.obtener_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.patch("/{pedido_id}/estado", response_model=PedidoResponse)
def actualizar_estado_pedido(pedido_id: int, estado: EstadoPedido):
    pedido = repo.obtener_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    pedido["estado"] = estado.value
    return pedido

@router.delete("/{pedido_id}", status_code=204)
def eliminar_pedido(pedido_id: int):
    eliminado = repo.eliminar(pedido_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return