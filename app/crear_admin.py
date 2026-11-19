import argparse
from getpass import getpass

from pydantic import ValidationError

from app.database import SessionLocal
from app.domain.auth import PASSWORD_MAX, PASSWORD_MIN, EmailDuplicado, Rol
from app.schemas.auth import Registro
from app.services.auth_service import registrar_usuario


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea una cuenta nueva con perfil administrador.")
    parser.add_argument("email")
    args = parser.parse_args()
    password = getpass("Contraseña: ")
    if password != getpass("Repite la contraseña: "):
        parser.error("Las contraseñas no coinciden.")
    try:
        datos = Registro(email=args.email, password=password)
    except ValidationError:
        parser.error(f"Indica un correo válido y una contraseña de {PASSWORD_MIN} a {PASSWORD_MAX} caracteres.")
    try:
        with SessionLocal() as db:
            registrar_usuario(db, datos.email, datos.password.get_secret_value(), rol=Rol.ADMIN)
    except EmailDuplicado:
        parser.error("El correo ya está en uso. Indica uno distinto para la cuenta administrativa.")
    print("Cuenta administrativa creada.")


if __name__ == "__main__":
    main()
