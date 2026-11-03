from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.pedido import PedidoCreate
from app.repositories.productos_repository import ProductosRepositorio
from app.repositories.pedidos_repository import PedidosRepositorio
from app.repositories.clientes_repository import ClientesRepositorio

def crear_pedido_servicio(pedido_data: PedidoCreate, db: Session):
    productos_repo = ProductosRepositorio(db)
    pedidos_repo = PedidosRepositorio(db)
    clientes_repo = ClientesRepositorio(db)

    cliente = clientes_repo.obtener_por_id(pedido_data.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    producto = productos_repo.obtener_por_id(pedido_data.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.stock < pedido_data.cantidad:
        raise HTTPException(status_code=409, detail="Stock insuficiente")

    monto_total = producto.precio * pedido_data.cantidad

    try:
        productos_repo.actualizar(producto.id, {"stock": producto.stock - pedido_data.cantidad})

        nuevo_pedido = {
            "cliente_id": pedido_data.cliente_id,
            "producto_id": pedido_data.producto_id,
            "cantidad": pedido_data.cantidad,
            "monto_total": monto_total,
            "estado": "pendiente"
        }

        resultado = pedidos_repo.guardar(nuevo_pedido)
        db.commit()
        return resultado

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al procesar el pedido. No se alteró el stock.")