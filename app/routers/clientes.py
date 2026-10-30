from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.schemas.pedido import PedidoResponse
from app.repositories.clientes_repository import ClientesRepositorio
from app.repositories.pedidos_repository import PedidosRepositorio

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    repo = ClientesRepositorio(db)
    return repo.guardar(cliente.model_dump())

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    repo = ClientesRepositorio(db)
    return repo.obtener_todos()

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    repo = ClientesRepositorio(db)
    cliente = repo.obtener_por_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/{cliente_id}/pedidos", response_model=list[PedidoResponse])
def obtener_pedidos_de_cliente(cliente_id: int, db: Session = Depends(get_db)):
    clientes_repo = ClientesRepositorio(db)
    pedidos_repo = PedidosRepositorio(db)
    
    cliente = clientes_repo.obtener_por_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
    todos = pedidos_repo.obtener_todas()
    return [p for p in todos if p.cliente_id == cliente_id]

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    repo = ClientesRepositorio(db)
    actualizado = repo.actualizar(cliente_id, cliente.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return actualizado

@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    repo = ClientesRepositorio(db)
    if not repo.eliminar(cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")