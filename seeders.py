from sqlalchemy import select

from app.database import SessionLocal
from app.domain.models import Categoria, Cliente, Pedido, Producto


def run_seeders():
    with SessionLocal.begin() as db:
        if any(db.scalar(select(modelo.id).limit(1)) is not None for modelo in (Categoria, Cliente, Producto, Pedido)):
            print("Ya existen datos de negocio. Se omitió la carga de demostración.")
            return

        cafe = Producto(nombre="Cafe Americano", precio=1500.0, stock=10, categoria=Categoria(nombre="Bebidas Calientes"))
        medialuna = Producto(nombre="Medialuna", precio=800.0, stock=15, categoria=Categoria(nombre="Pasteleria"))
        carlos = Cliente(nombre="Carlos", email="carlos@example.com")
        maria = Cliente(nombre="Maria", email="maria@example.com")
        db.add_all([cafe, medialuna, carlos, maria])
        db.flush()
        db.add_all([
            Pedido(cliente=carlos, producto_id=cafe.id, cantidad=2, monto_total=3000.0, estado="pendiente"),
            Pedido(cliente=maria, producto_id=medialuna.id, cantidad=1, monto_total=800.0, estado="pendiente"),
        ])

    print("Datos de demostración cargados.")


if __name__ == "__main__":
    run_seeders()
