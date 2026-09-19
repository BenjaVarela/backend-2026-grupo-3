from fastapi import APIRouter, HTTPException
from app.schemas.categoria import CategoriaProductoCreate, CategoriaProductoResponse
from app.repositories.categorias_repository import CategoriasRepository

router = APIRouter(prefix="/categorias", tags=["Categorias"])
repo = CategoriasRepository()

@router.post("/", response_model=CategoriaProductoResponse, status_code=201)
def crear_categoria(categoria: CategoriaProductoCreate):
    return repo.guardar(categoria.model_dump())

@router.get("/", response_model=list[CategoriaProductoResponse])
def listar_categorias():
    return repo.obtener_todos()

@router.get("/{categoria_id}", response_model=CategoriaProductoResponse)
def obtener_categoria(categoria_id: int):
    categoria = repo.obtener_por_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaProductoResponse)
def actualizar_categoria(categoria_id: int, categoria: CategoriaProductoCreate):
    actualizado = repo.actualizar(categoria_id, categoria.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return actualizado

@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int):
    eliminado = repo.eliminar(categoria_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return