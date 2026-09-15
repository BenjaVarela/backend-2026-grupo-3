from app.schemas.pedido import Pedido
from fastapi import HTTPException

db_pedidos = []

def crear_nuevo_pedido(pedido: Pedido):
    db_pedidos.append(pedido)
    return pedido

def obtener_pedidos():
    return db_pedidos