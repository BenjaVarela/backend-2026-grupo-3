from fastapi import APIRouter
from app.schemas.cliente import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])

db_clientes = []

@router.post("/", response_model=Cliente, status_code=201)
def crear_cliente(cliente: Cliente):
    db_clientes.append(cliente)
    return cliente

@router.get("/", response_model=list[Cliente])
def listar_clientes():
    return db_clientes