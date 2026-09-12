from fastapi import APIRouter, HTTPException
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