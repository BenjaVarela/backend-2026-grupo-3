db_pedidos = [
    {"id": 1, "id_cliente": 1, "id_producto": 1, "cantidad": 1, "monto_total": 2000.0, "estado": "completado"}
]

class PedidosRepository:
    def obtener_todos(self):
        return db_pedidos

    def obtener_por_id(self, pedido_id: int):
        for p in db_pedidos:
            if p["id"] == pedido_id:
                return p
        return None

    def guardar(self, datos: dict):
        nuevo_id = max([p["id"] for p in db_pedidos], default=0) + 1
        datos["id"] = nuevo_id
        db_pedidos.append(datos)
        return datos

    def actualizar(self, pedido_id: int, datos: dict):
        for i, p in enumerate(db_pedidos):
            if p["id"] == pedido_id:
                datos["id"] = pedido_id
                db_pedidos[i] = datos
                return datos
        return None

    def eliminar(self, pedido_id: int):
        for i, p in enumerate(db_pedidos):
            if p["id"] == pedido_id:
                db_pedidos.pop(i)
                return True
        return False