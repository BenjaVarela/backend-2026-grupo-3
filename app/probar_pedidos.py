from threading import Thread
from app.database import SessionLocal
from app.domain.models import Pedido, Producto
from app.schemas.pedido import PedidoCreate
from app.services import pedido_service


def pedir(producto_id, resultados):
    with SessionLocal() as db:
        try:
            pedido_service.crear_pedido_servicio(
                PedidoCreate(cliente_id=1, producto_id=producto_id, cantidad=1), db
            )
            resultados.append("ok")
        except Exception as e:
            resultados.append(getattr(e, "status_code", "error"))


with SessionLocal() as db:
    producto = Producto(nombre="Prueba", precio=1000.0, stock=1, categoria_id=1)
    db.add(producto)
    db.commit()
    producto_id = producto.id

resultados = []
hilos = [Thread(target=pedir, args=(producto_id, resultados)) for _ in range(2)]
for h in hilos:
    h.start()
for h in hilos:
    h.join()

with SessionLocal() as db:
    stock = db.get(Producto, producto_id).stock
    pedidos = db.query(Pedido).filter(Pedido.producto_id == producto_id).count()

print(resultados, "stock:", stock, "pedidos:", pedidos)

original = pedido_service.PedidosRepositorio.guardar


def guardar_con_fallo(self, datos, *, commit=True):
    raise RuntimeError("fallo forzado")


pedido_service.PedidosRepositorio.guardar = guardar_con_fallo

with SessionLocal() as db:
    db.add(Producto(nombre="Rollback", precio=500.0, stock=5, categoria_id=1))
    db.commit()
    rollback_id = db.query(Producto).filter(Producto.nombre == "Rollback").order_by(Producto.id.desc()).first().id

with SessionLocal() as db:
    try:
        pedido_service.crear_pedido_servicio(PedidoCreate(cliente_id=1, producto_id=rollback_id, cantidad=2), db)
    except Exception:
        pass

with SessionLocal() as db:
    print("stock tras fallo:", db.get(Producto, rollback_id).stock)

pedido_service.PedidosRepositorio.guardar = original