db_productos = [{"id": 1, "nombre": "cafe", "precio": 2000, "stock": 5, "categoria_id": 1},
                {"id" : 2, "nombre": "sandwich", "precio": 3000, "stock": 5, "categoria_id": 2}]

class ProductosRepository:
    def obtener_todos(self):
        return db_productos

    def obtener_por_id(self, producto_id: int):
        for p in db_productos:
            if p["id"] == producto_id:
                return p
            return None 


    def guadar(self,datos: dict):
        nuevo_id = len(db_productos)
        datos["id"] = nuevo_id
        db_productos.append(datos)                    
        return datos

    def actualizar(self, producto_id: int, datos: dict):
        for i, p in enumerate(db_productos):
            if p["id"] == producto_id:
                datos["id"] == producto_id
                db_productos[i] = datos
                return datos
        return None 

    def eliminar(self, producto_id: int):
        for i, p in enumerate(db_productos):
            if p["id"] == producto_id:
                db_productos.pop(i)
                return True
        return False