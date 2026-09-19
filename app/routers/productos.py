import math
from fastapi import APIRouter, HTTPException, Query
from app.schemas.producto import ProductoCreate, ProductoResponse
from app.repositories.productos_repository import ProductosRepository

router = APIRouter(prefix="/productos", tags=["Productos"])
repo = ProductosRepository()

@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate):
    return repo.guardar(producto.model_dump())

@router.get("/")
def listar_productos(
    categoria_id: int | None = Query(None, description="Filtrar por ID de categoría"),
    ordenar_precio: str | None = Query(None, description="asc o desc para ordenar"),
    pagina: int = Query(1, ge=1, description="Número de página"),
    limite: int = Query(10, ge=1, description="Cantidad de productos por página")
):
    productos = repo.obtener_todos()

    if categoria_id is not None:
        productos = [p for p in productos if p["categoria_id"] == categoria_id]

    if ordenar_precio == "asc":
        productos.sort(key=lambda x: x["precio"])
    elif ordenar_precio == "desc":
        productos.sort(key=lambda x: x["precio"], reverse=True)

    total = len(productos)
    total_paginas = math.ceil(total / limite) if total > 0 else 1
    inicio = (pagina - 1) * limite
    fin = inicio + limite
    productos_paginados = productos[inicio:fin]

    return {
        "total": total,
        "total_paginas": total_paginas,
        "pagina_actual": pagina,
        "data": productos_paginados
    }

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int):
    producto = repo.obtener_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoCreate):
    actualizado = repo.actualizar(producto_id, producto.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return actualizado

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    eliminado = repo.eliminar(producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return