from fastapi import APIRouter, HTTPException
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.repositories.clientes_repository import ClientesRepository

router = APIRouter(prefix="/clientes", tags=["Clientes"])
repo = ClientesRepository()

@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate):
    return repo.guardar(cliente.model_dump())

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes():
    return repo.obtener_todos()

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int):
    cliente = repo.obtener_por_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: ClienteCreate):
    actualizado = repo.actualizar(cliente_id, cliente.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return actualizado

@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(cliente_id: int):
    eliminado = repo.eliminar(cliente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return