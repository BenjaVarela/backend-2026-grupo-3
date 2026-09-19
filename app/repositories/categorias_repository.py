db_categorias = [
    {"id": 1, "nombre": "Bebidas Calientes", "descripcion": "Cafés, tés e infusiones"},
    {"id": 2, "nombre": "Repostería", "descripcion": "Pasteles, muffins y galletas"}
]

class CategoriasRepository:
    def obtener_todas(self):
        return db_categorias

    def obtener_por_id(self, categoria_id: int):
        for c in db_categorias:
            if c["id"] == categoria_id:
                return c
        return None

    def guardar(self, datos: dict):
        nuevo_id = max([c["id"] for c in db_categorias], default=0) + 1
        datos["id"] = nuevo_id
        db_categorias.append(datos)
        return datos

    def actualizar(self, categoria_id: int, datos: dict):
        for i, c in enumerate(db_categorias):
            if c["id"] == categoria_id:
                datos["id"] = categoria_id
                db_categorias[i] = datos
                return datos
        return None

    def eliminar(self, categoria_id: int):
        for i, c in enumerate(db_categorias):
            if c["id"] == categoria_id:
                db_categorias.pop(i)
                return True
        return False