import os
import smtplib
import ssl
from email.message import EmailMessage

def enviar_correo_recuperacion(destinatario: str, token: str) -> None:
    mensaje = EmailMessage()
    mensaje["Subject"] = "Recuperación de contraseña de Cafetería"
    mensaje["From"] = os.getenv("SMTP_FROM", "cafeteria@example.test")
    mensaje["To"] = destinatario
    mensaje.set_content(
        "Copia este código en el formulario de restablecimiento. Expira en 10 minutos.\n\n"
        f"{token}\n\nSi no pediste el cambio, puedes ignorar este mensaje.\n"
    )
    host = os.environ["SMTP_HOST"]
    port = int(os.getenv("SMTP_PORT", "587"))
    modo = os.getenv("SMTP_TLS", "starttls")
    contexto = ssl.create_default_context()
    if modo == "ssl":
        conexion = smtplib.SMTP_SSL(host, port, timeout=10, context=contexto)
    elif modo in {"starttls", "none"}:
        conexion = smtplib.SMTP(host, port, timeout=10)
    else:
        raise ValueError("SMTP_TLS debe ser starttls, ssl o none.")

    with conexion:
        if modo == "starttls":
            conexion.starttls(context=contexto)
        username = os.getenv("SMTP_USERNAME")
        if username:
            conexion.login(username, os.environ["SMTP_PASSWORD"])
        conexion.send_message(mensaje)
