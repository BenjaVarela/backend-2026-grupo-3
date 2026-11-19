import logging

from app.database import SessionLocal
from app.infrastructure.mail import enviar_correo_recuperacion
from app.infrastructure.security import TokensJWT
from app.services.auth_service import AuthServicio


logger = logging.getLogger(__name__)


def procesar_recuperacion(email: str, jwt: TokensJWT) -> None:
    try:
        with SessionLocal() as db:
            correo = AuthServicio(db, jwt).preparar_recuperacion(email)
        if correo:
            enviar_correo_recuperacion(*correo)
    except Exception as error:
        # Las excepciones SMTP pueden incluir datos del mensaje.
        logger.error("No se pudo procesar el correo de recuperación (%s).", type(error).__name__)
