from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse, EstadoPedido
from app.services.pedido_service import crear_pedido_servicio
from app.repositories.pedidos_repository import PedidosRepositorio

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResponse, status_code=201)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return crear_pedido_servicio(pedido, db)

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(estado: EstadoPedido | None = Query(None), db: Session = Depends(get_db)):
    repo = PedidosRepositorio(db)
    pedidos = repo.obtener_todas()
    if estado:
        pedidos = [p for p in pedidos if p.estado == estado.value or p.estado == estado]
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoResponse)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    repo = PedidosRepositorio(db)
    pedido = repo.obtener_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.patch("/{pedido_id}/estado", response_model=PedidoResponse)
def actualizar_estado_pedido(pedido_id: int, estado: EstadoPedido, db: Session = Depends(get_db)):
    repo = PedidosRepositorio(db)
    pedido = repo.obtener_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return repo.actualizar(pedido_id, {"estado": estado.value})

@router.delete("/{pedido_id}", status_code=204)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    repo = PedidosRepositorio(db)
    if not repo.eliminar(pedido_id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")