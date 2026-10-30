from fastapi import HTTPException, status
from app.schemas.pedido import PedidoCreate
from app.repositories.productos_repository import ProductosRepository
from app.repositories.pedidos_repository import PedidosRepository

productos_repo = ProductosRepository()
pedidos_repo = PedidosRepository()

def crear_pedido_servicio(pedido_data: PedidoCreate):
    producto = productos_repo.obtener_por_id(pedido_data.id_producto)
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
        
    if producto["stock"] < pedido_data.cantidad:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Stock insuficiente para realizar el pedido"
        )
        
    # Calcular total y descontar stock
    monto_total = producto["precio"] * pedido_data.cantidad
    producto["stock"] -= pedido_data.cantidad
    productos_repo.actualizar(producto["id"], producto)
    
    nuevo_pedido = {
        "id_cliente": pedido_data.id_cliente,
        "id_producto": pedido_data.id_producto,
        "cantidad": pedido_data.cantidad,
        "monto_total": monto_total,
        "estado": "pendiente"
    }
    
    return pedidos_repo.guardar(nuevo_pedido)