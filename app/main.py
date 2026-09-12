from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routers import productos, categorias, clientes, pedidos

app = FastAPI(title="API Cafeteria",
    description="API REST para la gestion de pedidos e inventario de la cafeteria",
    version="1.0.0")

app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": "Datos de entrada invalidos",
                "details": exc.errors()}})

@app.get("/", tags=["Health Check"])
def root():
    return {"mensaje": "de que la cafeteria funcione correctamente"}