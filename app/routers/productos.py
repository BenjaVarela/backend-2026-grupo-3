from fastapi import APIRouter
from app.schemas.producto import Producto

router = APIRouter(prefix="/productos", tags=["Productos"])

db_productos = []

@router.post("/", response_model=Producto, status_code=201)
def crear_producto(producto: Producto):
    db_productos.append(producto)
    return producto

@router.get("/", response_model=list[Producto])
def listar_productos():
    return db_productos