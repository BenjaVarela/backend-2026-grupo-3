db_categorias = [{"id": 1, "nombre": "Bebidas Calientes", "descripcion": "Cafés, tés e infusiones"},
    {"id": 2, "nombre": "Repostería", "descripcion": "Pasteles, muffins y galletas"}]

class CategoriasRepository:
    def obtener_todas(self):
        return db_categorias

    def obtener_por_id(self, categoria_id: int):
        for c in db_categorias:
            if c["id"] == categoria_id:
                return c
        return None

    def actualizar(self, categorias_id: int, datos: dict):
                for i, p in enumerate(db_categorias):
                    if p["id"] == categorias_id:
                        datos["id"] == categorias_id
                        db_categorias[i] = datos
                        return datos
                return None
    
    def eliminar(self, categorias_id: int):
                for i, p in enumerate(db_categorias):
                    if p["id"] == categorias_id:
                        db_categorias.pop(i)
                        return True
                return False
    