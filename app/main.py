from fastapi import FastAPI
from app.routers import categorias, clientes, productos, pedidos
from app.excepciones import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="API Cafetería Universitaria")

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(categorias.router)
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(pedidos.router)