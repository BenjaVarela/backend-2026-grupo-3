from time import time
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, Response
from fastapi.security import APIKeyCookie

from app.config import allowed_origins, cookie_secure
from app.domain.auth import ACCESS_TTL
from app.schemas.auth import AccessResponse
from app.services.auth_service import SesionEmitida


COOKIE = "refresh_token"
COOKIE_PATH = "/auth"
refresh_cookie = APIKeyCookie(
    name=COOKIE,
    auto_error=False,
    description="Cookie HttpOnly que se recibe al iniciar o renovar una sesión.",
)
RefreshCookie = Annotated[str | None, Depends(refresh_cookie)]


def verificar_origen(request: Request) -> None:
    origen = request.headers.get("origin")
    if origen is not None and origen not in allowed_origins():
        raise HTTPException(status_code=403, detail="Origen no permitido.")


def proteger_cookie(
    x_csrf_protection: Annotated[str | None, Header(description="Enviar el valor 1.")] = None,
) -> None:
    if x_csrf_protection != "1":
        raise HTTPException(status_code=403, detail="Falta la cabecera de protección CSRF.")


def entregar_sesion(response: Response, sesion: SesionEmitida) -> AccessResponse:
    response.headers["Cache-Control"] = "no-store"
    response.set_cookie(
        key=COOKIE,
        value=sesion.refresh_token,
        max_age=max(0, sesion.refresh_expira - int(time())),
        path=COOKIE_PATH,
        httponly=True,
        secure=cookie_secure(),
        samesite="lax",
    )
    return AccessResponse(access_token=sesion.access_token, expires_in=ACCESS_TTL)


def borrar_cookie(response: Response) -> None:
    response.delete_cookie(COOKIE, path=COOKIE_PATH, httponly=True, secure=cookie_secure(), samesite="lax")
