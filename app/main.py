from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routers import productos, categorias, clientes, pedidos

app = FastAPI(
    title="API Cafeteria",
    description="API REST para la gestión de pedidos e inventario de la cafetería",
    version="1.0.0"
)

# Conectar los 4 routers a la aplicación
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(clientes.router)
app.include_router(pedidos.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": "Datos de entrada inválidos",
                "details": exc.errors()
            }
        }
    )

@app.get("/", tags=["Health Check"])
def root():
    return {"mensaje": "La API de la cafetería está funcionando correctamente"}