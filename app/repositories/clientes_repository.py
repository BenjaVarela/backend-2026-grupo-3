from sqlalchemy.orm import Session
from app.domain.models import Cliente

class ClientesRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self):
        return self.db.query(Cliente).all()

    def obtener_por_id(self, cliente_id: int):
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def guardar(self, datos: dict):
        nuevo = Cliente(**datos)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, cliente_id: int, datos: dict):
        cliente = self.obtener_por_id(cliente_id)
        if not cliente:
            return None
        for key, value in datos.items():
            setattr(cliente, key, value)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar(self, cliente_id: int):
        cliente = self.obtener_por_id(cliente_id)
        if not cliente:
            return False
        self.db.delete(cliente)
        self.db.commit()
        return True