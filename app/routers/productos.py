from fastapi import APIRouter, HTTPException, Query
from app.schemas.producto import ProductoCreate, ProductoResponse
from app.repositories.productos_repository import ProductosRepository

router = APIRouter(prefix="/productos", tags=["Productos"])
repo = ProductosRepository()

@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate):
    return repo.guardar(producto.model_dump())

@router.get("/", response_model=list[ProductoResponse])
def listar_productos(
    skip: int = Query(0, description="Elementos a saltar"),
    limit: int = Query(10, description="Límite por página"),
    buscar: str | None = Query(None, description="Filtro por nombre")
):
    productos = repo.obtener_todos()
    if buscar:
        productos = [p for p in productos if buscar.lower() in p["nombre"].lower()]
    return productos[skip : skip + limit]

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