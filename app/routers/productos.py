import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.repositories.productos_repository import ProductosRepositorio
from app.repositories.categorias_repository import CategoriasRepositorio

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    repo = ProductosRepositorio(db)
    categorias_repo = CategoriasRepositorio(db)
    
    categoria = categorias_repo.obtener_por_id(producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoría no existe.")
    return repo.guardar(producto.model_dump())

@router.get("/")
def listar_productos(
    categoria_id: Optional[int] = Query(None),
    ordenar_precio: Optional[str] = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    repo = ProductosRepositorio(db)
    productos = repo.obtener_todas()

    if categoria_id is not None:
        productos = [p for p in productos if p.categoria_id == categoria_id]
    if ordenar_precio == "asc":
        productos.sort(key=lambda x: x.precio)
    elif ordenar_precio == "desc":
        productos.sort(key=lambda x: x.precio, reverse=True)

    total = len(productos)
    total_paginas = math.ceil(total / limite) if total > 0 else 1
    inicio = (pagina - 1) * limite
    fin = inicio + limite

    return {
        "total": total,
        "total_paginas": total_paginas,
        "pagina_actual": pagina,
        "data": productos[inicio:fin]
    }

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    repo = ProductosRepositorio(db)
    producto = repo.obtener_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    repo = ProductosRepositorio(db)
    categorias_repo = CategoriasRepositorio(db)
    datos = producto.model_dump(exclude_unset=True)
    
    if "categoria_id" in datos and datos["categoria_id"] is not None:
        if not categorias_repo.obtener_por_id(datos["categoria_id"]):
            raise HTTPException(status_code=400, detail="Categoría no existe.")
            
    actualizado = repo.actualizar(producto_id, datos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return actualizado

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    repo = ProductosRepositorio(db)
    if not repo.eliminar(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")