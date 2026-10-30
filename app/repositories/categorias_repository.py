from sqlalchemy.orm import Session
from app.domain.models import Categoria

class CategoriasRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self):
        return self.db.query(Categoria).all()

    def obtener_por_id(self, categoria_id: int):
        return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()

    def guardar(self, datos: dict):
        nueva = Categoria(**datos)
        self.db.add(nueva)
        self.db.commit()
        self.db.refresh(nueva)
        return nueva

    def actualizar(self, categoria_id: int, datos: dict):
        categoria = self.obtener_por_id(categoria_id)
        if not categoria:
            return None
        for key, value in datos.items():
            setattr(categoria, key, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar(self, categoria_id: int):
        categoria = self.obtener_por_id(categoria_id)
        if not categoria:
            return False
        self.db.delete(categoria)
        self.db.commit()
        return True