from fastapi import APIRouter
from app.schemas.categoria import Categoria

router = APIRouter(prefix="/categorias", tags=["Categorías"])

db_categorias = []

@router.post("/", response_model=Categoria, status_code=201)
def crear_categoria(categoria: Categoria):
    db_categorias.append(categoria)
    return categoria

@router.get("/", response_model=list[Categoria])
def listar_categorias():
    return db_categoriasfrom fastapi import APIRouter, HTTPException
from app.repositories.categorias_repository import CategoriasRepository

router = APIRouter()
repo = CategoriasRepository()

@router.get("")
def listar_categorias():
    return repo.obtener_todas()

@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    categoria = repo.obtener_por_id(categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "RESOURCE_NOT_FOUND", "message": "Categoria no encontrada", "details": []}}
        )
    return categoria