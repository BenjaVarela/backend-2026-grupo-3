from fastapi import APIRouter, HTTPException
from app.repositories.clientes_repository import ClientesRepository

router = APIRouter()
repo = ClientesRepository()

@router.get("")
def listar_clientes():
    return repo.obtener_todos()

@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int):
    cliente = repo.obtener_por_id(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "RESOURCE_NOT_FOUND", "message": "Cliente no encontrado", "details": []}}
        )
    return cliente