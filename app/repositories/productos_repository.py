from sqlalchemy.orm import Session
from app.domain.models import Producto

class ProductosRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self):
        return self.db.query(Producto).all()

    def obtener_por_id(self, producto_id: int):
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def guardar(self, datos: dict):
        nuevo = Producto(**datos)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, producto_id: int, datos: dict):
        producto = self.obtener_por_id(producto_id)
        if not producto:
            return None
        for key, value in datos.items():
            setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar(self, producto_id: int):
        producto = self.obtener_por_id(producto_id)
        if not producto:
            return False
        self.db.delete(producto)
        self.db.commit()
        return True