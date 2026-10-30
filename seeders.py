from app.database import SessionLocal
from app.domain.models import Categoria, Cliente, Producto, Pedido

def run_seeders():
    db = SessionLocal()
    
    if not db.query(Categoria).first():
        db.add_all([
            Categoria(nombre="Bebidas Calientes"),
            Categoria(nombre="Pasteleria")
        ])
        db.commit()

    if not db.query(Cliente).first():
        db.add_all([
            Cliente(nombre="Carlos", email="carlos@correo.com"),
            Cliente(nombre="Maria", email="maria@correo.com")
        ])
        db.commit()

    if not db.query(Producto).first():
        db.add_all([
            Producto(nombre="Cafe Americano", precio=1500.0, stock=10, categoria_id=1),
            Producto(nombre="Medialuna", precio=800.0, stock=15, categoria_id=2)
        ])
        db.commit()

    if not db.query(Pedido).first():
        db.add_all([
            Pedido(cliente_id=1, producto_id=1, cantidad=2, monto_total=3000.0, estado="pendiente"),
            Pedido(cliente_id=2, producto_id=2, cantidad=1, monto_total=800.0, estado="pendiente")
        ])
        db.commit()

    db.close()

if __name__ == "__main__":
    run_seeders()