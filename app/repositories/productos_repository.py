from sqlalchemy.orm import Session
from app.domain.models import Producto


class ProductosRepositorio:
    def __init__(self, db: Session):
        self.db = db
        self.model = Producto

    def obtener_por_id(self, producto_id: int, *, bloquear: bool = False) -> Producto | None:
        """Con bloquear=True, lee el estado actual y bloquea la fila hasta terminar la transacción."""
        consulta = self.db.query(self.model).filter(self.model.id == producto_id)
        if bloquear:
            consulta = consulta.populate_existing().with_for_update()
        return consulta.first()

    def obtener_todas(self):
        return self.db.query(self.model).all()

    def guardar(self, datos: dict):
        db_item = self.model(**datos)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def actualizar(self, producto_id: int, datos: dict, *, commit: bool = True):
        db_item = self.obtener_por_id(producto_id)
        if not db_item:
            return None

        for key, value in datos.items():
            setattr(db_item, key, value)

        if commit:
            self.db.commit()
            self.db.refresh(db_item)
        else:
            self.db.flush()

        return db_item

    def eliminar(self, producto_id: int):
        db_item = self.obtener_por_id(producto_id)
        if not db_item:
            return False
        self.db.delete(db_item)
        self.db.commit()
        return True

    def obtener_con_filtros_y_paginacion(self, categoria_id=None, ordenar_por=None, direccion="asc", pagina=1, limite=20):
        query = self.db.query(self.model)

        if categoria_id is not None:
            query = query.filter(self.model.categoria_id == categoria_id)

        if ordenar_por and hasattr(self.model, ordenar_por):
            columna = getattr(self.model, ordenar_por)
            if direccion == "desc":
                query = query.order_by(columna.desc())
            else:
                query = query.order_by(columna.asc())

        total = query.count()

        items = query.offset((pagina - 1) * limite).limit(limite).all()

        return items, total
