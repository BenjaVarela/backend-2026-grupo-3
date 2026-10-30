from sqlalchemy.orm import Session
from app.domain.models import Pedido

class PedidosRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self):
        return self.db.query(Pedido).all()

    def obtener_por_id(self, pedido_id: int):
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def guardar(self, datos: dict):
        nuevo = Pedido(**datos)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, pedido_id: int, datos: dict):
        pedido = self.obtener_por_id(pedido_id)
        if not pedido:
            return None
        for key, value in datos.items():
            setattr(pedido, key, value)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def eliminar(self, pedido_id: int):
        pedido = self.obtener_por_id(pedido_id)
        if not pedido:
            return False
        self.db.delete(pedido)
        self.db.commit()
        return True