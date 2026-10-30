import math
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.repositories.productos_repository import ProductosRepository
from app.repositories.categorias_repository import CategoriasRepository

router = APIRouter(prefix="/productos", tags=["Productos"])
repo = ProductosRepository()
categorias_repo = CategoriasRepository()

@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate):
    datos = producto.model_dump()
    categoria = categorias_repo.obtener_por_id(datos["id_categoria"])
    if not categoria:
        raise HTTPException(status_code=400, detail=f"La categoría con ID {datos['id_categoria']} no existe.")
    return repo.guardar(datos)

@router.get("/")
def listar_productos(
    id_categoria: Optional[int] = Query(None, description="Filtrar por ID de categoría"),
    ordenar_precio: Optional[str] = Query(None, description="asc o desc para ordenar"),
    pagina: int = Query(1, ge=1, description="Número de página"),
    limite: int = Query(10, ge=1, description="Cantidad de productos por página")
):
    productos = repo.obtener_todos()

    # Filtrado unificado por id_categoria
    if id_categoria is not None:
        productos = [
            p for p in productos 
            if (p.get("id_categoria") if isinstance(p, dict) else getattr(p, "id_categoria", None)) == id_categoria
        ]

    # Ordenamiento por precio
    if ordenar_precio == "asc":
        productos.sort(key=lambda x: x["precio"] if isinstance(x, dict) else x.precio)
    elif ordenar_precio == "desc":
        productos.sort(key=lambda x: x["precio"] if isinstance(x, dict) else x.precio, reverse=True)

    # Paginación
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
def actualizar_producto(producto_id: int, producto: ProductoUpdate):
    datos = producto.model_dump(exclude_unset=True)
    if "id_categoria" in datos and datos["id_categoria"] is not None:
        categoria = categorias_repo.obtener_por_id(datos["id_categoria"])
        if not categoria:
            raise HTTPException(status_code=400, detail=f"La categoría con ID {datos['id_categoria']} no existe.")

    actualizado = repo.actualizar(producto_id, datos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return actualizado

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    eliminado = repo.eliminar(producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return