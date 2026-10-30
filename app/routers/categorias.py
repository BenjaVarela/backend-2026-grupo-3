from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.categoria import CategoriaProductoCreate, CategoriaProductoResponse
from app.repositories.categorias_repository import CategoriasRepositorio

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.post("/", response_model=CategoriaProductoResponse, status_code=201)
def crear_categoria(categoria: CategoriaProductoCreate, db: Session = Depends(get_db)):
    repo = CategoriasRepositorio(db)
    return repo.guardar(categoria.model_dump())

@router.get("/", response_model=list[CategoriaProductoResponse])
def listar_categorias(db: Session = Depends(get_db)):
    repo = CategoriasRepositorio(db)
    return repo.obtener_todas()

@router.get("/{categoria_id}", response_model=CategoriaProductoResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    repo = CategoriasRepositorio(db)
    categoria = repo.obtener_por_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaProductoResponse)
def actualizar_categoria(categoria_id: int, categoria: CategoriaProductoCreate, db: Session = Depends(get_db)):
    repo = CategoriasRepositorio(db)
    actualizado = repo.actualizar(categoria_id, categoria.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return actualizado

@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    repo = CategoriasRepositorio(db)
    if not repo.eliminar(categoria_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")