db_pedidos = [{"id": 1, "cliente_id": 1, "total": 3800, "estado": "completado"}]

class PedidosRepository:
    def obtener_todos(self):
        return db_pedidos

    def obtener_por_id(self, pedido_id: int):
        for p in db_pedidos:
            if p["id"] == pedido_id:
                return p
        return None

    def guardar(self, datos: dict):
        nuevo_id = len(db_pedidos) + 1
        datos["id"] = nuevo_id
        db_pedidos.append(datos)
        return datos

    def actualizar(self, pedidos_id: int, datos: dict):
            for i, p in enumerate(db_pedidos):
                if p["id"] == pedidos_id:
                    datos["id"] == pedidos_id
                    db_pedidos[i] = datos
                    return datos
            return None

    def eliminar(self, pedidos_id: int):
            for i, p in enumerate(db_pedidos):
                if p["id"] == pedidos_id:
                    db_pedidos.pop(i)
                    return True
            return False