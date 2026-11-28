from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import allowed_origins, jwt_secret
from app.dependencies import DB
from app.excepciones import http_exception_handler, validation_exception_handler, integridad_exception_handler
from app.routers import auth, categorias, clientes, pedidos, productos


@asynccontextmanager
async def lifespan(app: FastAPI):
    jwt_secret()
    yield


app = FastAPI(title="API Cafetería Universitaria v3", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Protection"],
)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integridad_exception_handler)
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(pedidos.router)


@app.get("/health", tags=["Operación"], responses={503: {"description": "Base de datos no disponible."}})
def health(db: DB):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Base de datos no disponible.") from None
    return {"status": "ok"}
