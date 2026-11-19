from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response

from app.dependencies import DB, RESPUESTA_401, ServicioAuth, UsuarioActual, tokens_jwt
from app.domain.auth import CredencialInvalida, EmailDuplicado
from app.http_security import RefreshCookie, borrar_cookie, entregar_sesion, proteger_cookie, verificar_origen
from app.infrastructure.security import TokensJWT
from app.schemas.auth import AccessResponse, Identificador, Login, Mensaje, Registro, Restablecimiento, UsuarioResponse
from app.services.auth_service import registrar_usuario
from app.services.recuperacion import procesar_recuperacion


router = APIRouter(prefix="/auth", tags=["Autenticación"])
VALIDAR_ORIGEN = [Depends(verificar_origen)]
PROTEGER_COOKIE = [Depends(verificar_origen), Depends(proteger_cookie)]
RESPUESTA_CSRF = {403: {"description": "Origen o cabecera CSRF inválidos."}}


@router.post("/registro", response_model=UsuarioResponse, status_code=201, responses={409: {"description": "Correo en uso."}})
def registro(datos: Registro, db: DB):
    try:
        return registrar_usuario(db, datos.email, datos.password.get_secret_value())
    except EmailDuplicado:
        raise HTTPException(status_code=409, detail="El correo ya está registrado.") from None


@router.post(
    "/login",
    response_model=AccessResponse,
    dependencies=VALIDAR_ORIGEN,
    responses=RESPUESTA_401 | RESPUESTA_CSRF,
)
def login(datos: Login, servicio: ServicioAuth, response: Response):
    try:
        sesion = servicio.login(datos.email, datos.password.get_secret_value())
    except CredencialInvalida:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.") from None
    return entregar_sesion(response, sesion)


@router.get("/me", response_model=UsuarioResponse, responses=RESPUESTA_401)
def me(usuario: UsuarioActual):
    return usuario


@router.post(
    "/refresh",
    response_model=AccessResponse,
    dependencies=PROTEGER_COOKIE,
    responses=RESPUESTA_401 | RESPUESTA_CSRF,
)
def refresh(token: RefreshCookie, servicio: ServicioAuth, response: Response):
    try:
        if not token or len(token) != 43:
            raise CredencialInvalida
        sesion = servicio.renovar(token)
    except CredencialInvalida:
        raise HTTPException(status_code=401, detail="Sesión inválida o vencida.") from None
    return entregar_sesion(response, sesion)


@router.post("/logout", status_code=204, dependencies=PROTEGER_COOKIE, responses=RESPUESTA_CSRF)
def logout(token: RefreshCookie, servicio: ServicioAuth):
    if token and len(token) == 43:
        servicio.logout(token)
    response = Response(status_code=204)
    borrar_cookie(response)
    return response


@router.post("/recuperacion", response_model=Mensaje, status_code=202)
def recuperacion(datos: Identificador, tareas: BackgroundTasks, jwt: Annotated[TokensJWT, Depends(tokens_jwt)]):
    tareas.add_task(procesar_recuperacion, datos.email, jwt)
    return Mensaje(mensaje="Si la cuenta puede recuperarse, recibirás un correo con las instrucciones.")


@router.post("/restablecer", status_code=204, responses={400: {"description": "JWT inválido, vencido o consumido."}})
def restablecer(datos: Restablecimiento, servicio: ServicioAuth):
    try:
        servicio.restablecer(datos.token.get_secret_value(), datos.nueva_password.get_secret_value())
    except CredencialInvalida:
        raise HTTPException(status_code=400, detail="Código de recuperación inválido o vencido.") from None
