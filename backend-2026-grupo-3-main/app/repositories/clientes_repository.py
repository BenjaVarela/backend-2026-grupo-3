db_clientes = [
    {"id": 1, "nombre": "persona 1", "email": "persona1@email.com", "telefono": "912345678"},
    {"id": 2, "nombre": "persona 2", "email": "persona2@email.com", "telefono": "987654321"}
]

class ClientesRepository:
    def obtener_todos(self):
        return db_clientes

    def obtener_por_id(self, cliente_id: int):
        for c in db_clientes:
            if c["id"] == cliente_id:
                return c
        return None

    def guardar(self, datos: dict):
        nuevo_id = max([c["id"] for c in db_clientes], default=0) + 1
        datos["id"] = nuevo_id
        db_clientes.append(datos)
        return datos

    def actualizar(self, cliente_id: int, datos: dict):
        for i, c in enumerate(db_clientes):
            if c["id"] == cliente_id:
                datos["id"] = cliente_id
                db_clientes[i] = datos
                return datos
        return None

    def eliminar(self, cliente_id: int):
        for i, c in enumerate(db_clientes):
            if c["id"] == cliente_id:
                db_clientes.pop(i)
                return True
        return False