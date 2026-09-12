from fastapi import APIRouter, HTTPException
from app.repositories.productos_repository import ProductosRepository
from app.schemas.producto import ProductoCreate

router = APIRouter()
repo = ProductosRepository()

@router.get("")
def listar_productos(categoria_id: int = None, ordenar_por: str = "id", direccion: str = "asc", pagina: int = 1, limite: int = 10):
    items = repo.obtener_todos()

    if categoria_id is not None:
        filtrados = []
        for p in items:
            if p.get("categoria_id") == categoria_id:
                filtrados.append(p)
        items = filtrados

    reverso = True if direccion == "desc" else False
    items = sorted(items, key=lambda x: x.get(ordenar_por, 0), reverse=reverso)

    total = len(items)
    inicio = (pagina - 1) * limite
    fin = inicio + limite
    items_paginados = items[inicio:fin]
    
    total_paginas = (total + limite - 1) // limite if total > 0 else 1

    return {
        "items": items_paginados,
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "total_paginas": total_paginas
    }

@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    producto = repo.obtener_por_id(producto_id)
    if not producto:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "RESOURCE_NOT_FOUND", "message": "Producto no encontrado", "details": []}}
        )
    return producto

@router.post("", status_code=201)
def crear_producto(producto: ProductoCreate):
    return repo.guardar(producto.model_dump())

@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, producto: ProductoCreate):
    actualizado = repo.actualizar(producto_id, producto.model_dump())
    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "RESOURCE_NOT_FOUND", "message": "Producto no encontrado", "details": []}}
        )
    return actualizado

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    borrado = repo.eliminar(producto_id)
    if not borrado:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "RESOURCE_NOT_FOUND", "message": "Producto no encontrado", "details": []}}
        )
    return None