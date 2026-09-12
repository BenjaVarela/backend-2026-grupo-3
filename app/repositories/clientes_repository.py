db_clientes = [{"id": 1, "nombre": "persona 1", "email": "persona1@email.com", "telefono": "912345678"},
    {"id": 2, "nombre": "persona 2", "email": "persona2@email.com", "telefono": "987654321"}]

class ClientesRepository:
    def obtener_todos(self):
        return db_clientes

    def obtener_por_id(self, cliente_id: int):
        for c in db_clientes:
            if c["id"] == cliente_id:
                return c
        return None

    def actualizar(self, clientes_id: int, datos: dict):
                for i, p in enumerate(db_clientes):
                    if p["id"] == clientes_id_id:
                        datos["id"] == clientes_id
                        db_clientes[i] = datos
                        return datos
                return None
    
    def eliminar(self, clientes_id: int):
                for i, p in enumerate(db_clientes):
                    if p["id"] == clientes_id:
                        db_clientes.pop(i)
                        return True
                return False