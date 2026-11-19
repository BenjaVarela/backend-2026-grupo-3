import re
from functools import cache
from hashlib import sha256
from secrets import token_urlsafe

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from argon2.low_level import Type

from app.domain.auth import CredencialInvalida


_HASHER = PasswordHasher(type=Type.ID)
_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return _HASHER.hash(password)


@cache
def _hash_ficticio() -> str:
    return hash_password(token_urlsafe(32))


def verificar_password(password: str, password_hash: str | None) -> bool:
    try:
        return _HASHER.verify(password_hash or _hash_ficticio(), password)
    except VerificationError:
        return False


def necesita_rehash(password_hash: str) -> bool:
    return _HASHER.check_needs_rehash(password_hash)


def hash_refresh(token: str) -> str:
    return sha256(token.encode()).hexdigest()


class TokensJWT:
    def __init__(self, secret: str):
        self.secret = secret

    def emitir(self, usuario_id: int, proposito: str, expira: int, **claims) -> str:
        return jwt.encode(
            {"sub": str(usuario_id), "type": proposito, "exp": expira, **claims},
            self.secret,
            algorithm=_ALGORITHM,
        )

    def validar(self, token: str, proposito: str, *requeridos: str) -> dict:
        try:
            claims = jwt.decode(
                token,
                self.secret,
                algorithms=[_ALGORITHM],
                options={"require": ["sub", "exp", "type", *requeridos]},
            )
        except jwt.InvalidTokenError:
            raise CredencialInvalida from None

        if (
            claims["type"] != proposito
            or type(claims["exp"]) is not int
            or not re.fullmatch(r"[1-9][0-9]{0,9}", claims["sub"])
            or int(claims["sub"]) > 2_147_483_647
        ):
            raise CredencialInvalida
        return claims
