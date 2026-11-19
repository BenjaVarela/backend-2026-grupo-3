from enum import StrEnum


class Rol(StrEnum):
    USUARIO = "usuario"
    ADMIN = "admin"


class CredencialInvalida(Exception):
    pass


class EmailDuplicado(Exception):
    pass


def normalizar_email(email: str) -> str:
    return email.casefold()


PASSWORD_MIN = 12
PASSWORD_MAX = 128
ACCESS_TTL = 15 * 60
REFRESH_TTL = 7 * 24 * 60 * 60
RESET_TTL = 10 * 60
RESET_INTERVAL = 60
LOGIN_MAX_ATTEMPTS = 5
LOGIN_BLOCK_TTL = 15 * 60
