from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
                "details": []
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detalles = []
    for error in exc.errors():
        ubicacion = error["loc"]
        if error["type"] == "extra_forbidden":
            ubicacion = ubicacion[:-1]
        detalles.append({"loc": ubicacion, "type": error["type"]})

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": "Los datos no cumplen el esquema o las validaciones declaradas",
                "details": detalles
            }
        }
    )

async def integridad_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "CONFLICT",
                "messaje": "El registro ya existe o rompe una relacion",
                "details": [],
            } 
        },
    )
