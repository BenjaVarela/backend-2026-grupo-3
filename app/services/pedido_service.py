from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.pedido import PedidoCreate
from app.repositories.productos_repository import ProductosRepositorio
from app.repositories.pedidos_repository import PedidosRepositorio

def crear_pedido_servicio(pedido_data: PedidoCreate, db: Session):
    productos_repo = ProductosRepositorio(db)
    pedidos_repo = PedidosRepositorio(db)

    producto = productos_repo.obtener_por_id(pedido_data.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.stock < pedido_data.cantidad:
        raise HTTPException(status_code=409, detail="Stock insuficiente")

    monto_total = producto.precio * pedido_data.cantidad
    
    productos_repo.actualizar(producto.id, {"stock": producto.stock - pedido_data.cantidad})

    nuevo_pedido = {
        "cliente_id": pedido_data.cliente_id,
        "producto_id": pedido_data.producto_id,
        "cantidad": pedido_data.cantidad,
        "monto_total": monto_total,
        "estado": "pendiente"
    }
    return pedidos_repo.guardar(nuevo_pedido)