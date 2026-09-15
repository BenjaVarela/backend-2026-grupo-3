from fastapi import HTTPException, status
from app.repositories.productos_repository import productos_db
from app.repositories.pedidos_repository import pedidos_db

def crear_pedido_servicio(pedido_data):
    producto = productos_db.get(pedido_data.producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Producto no encontrado", "codigo": 404}
        )
    
    if producto["stock"] < pedido_data.cantidad:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "Stock insuficiente para realizar el pedido", "codigo": 409}
        )
    
    monto_total = producto["precio"] * pedido_data.cantidad
    
    producto["stock"] -= pedido_data.cantidad
    
    nuevo_pedido = {
        "id": len(pedidos_db) + 1,
        "producto_id": pedido_data.producto_id,
        "cantidad": pedido_data.cantidad,
        "monto_total": monto_total
    }
    pedidos_db[nuevo_pedido["id"]] = nuevo_pedido
    
    return nuevo_pedido