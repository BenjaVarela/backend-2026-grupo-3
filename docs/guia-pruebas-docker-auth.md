# Guía de pruebas de Docker y autenticación

| Cambio | Dónde revisar |
| --- | --- |
| Docker Compose con API, PostgreSQL, Adminer y Mailpit. Volumen de datos, chequeos de disponibilidad y servicio de migración. | [docker-compose.yml](../docker-compose.yml), [Dockerfile](../docker/Dockerfile), [.env.example](../.env.example) |
| API ejecutada con usuario sin privilegios, dependencias fijadas y archivos locales excluidos de la imagen. | [Dockerfile](../docker/Dockerfile), [requirements.txt](../requirements.txt), [.dockerignore](../.dockerignore) |
| Registro, login con Argon2id, bloqueo de intentos y acceso según rol. Las cuentas de acceso son independientes de los clientes comerciales. | [Rutas](../app/routers/auth.py), [esquemas](../app/schemas/auth.py), [permisos](../app/dependencies.py), [comando administrativo](../app/crear_admin.py) |
| Access JWT, cookie refresh, rotación, protección CSRF y logout. | [Servicio](../app/services/auth_service.py), [transporte HTTP](../app/http_security.py), [firma y hashes](../app/infrastructure/security.py) |
| Recuperación por correo con JWT de un solo uso y revocación de sesiones. | [Recuperación](../app/services/recuperacion.py), [servicio de autenticación](../app/services/auth_service.py), [migración](../alembic/versions/71fd6e842b19_agrega_autenticacion.py) |

## Preparar un entorno individual

1. Copia `.env.example` a `.env` si aún no tienes ese archivo. Completa `POSTGRES_PASSWORD` y `JWT_SECRET` con valores aleatorios distintos. Revisa la [configuración del README](../README.md#4-inicio-con-docker-compose).
2. Usa un nombre de proyecto Compose exclusivo para ti durante estas pruebas. Reemplaza `cafeteria-pruebas` si ya lo ocupaste para otro propósito. Si hay otro entorno en marcha, detén ese entorno o define puertos libres en `.env` y usa sus valores en las URLs.
3. Levanta el entorno y verifica la migración.

   ```sh
   docker compose -p cafeteria-pruebas config --quiet
   docker compose -p cafeteria-pruebas up -d --build --wait
   docker compose -p cafeteria-pruebas ps -a
   docker compose -p cafeteria-pruebas exec web python -m alembic current
   docker compose -p cafeteria-pruebas exec web python -m alembic check
   docker compose -p cafeteria-pruebas exec web python seeders.py
   docker compose -p cafeteria-pruebas exec web python -m app.crear_admin admin-pruebas@example.com
   ```

   Comprueba que la API esté saludable y que `migrate` termine con código 0. Alembic debe mostrar `71fd6e842b19 (head)` y no detectar cambios pendientes. Anota la contraseña de prueba que ingreses para la cuenta administrativa.

## Ejecutar las pruebas

Abre [Swagger](http://127.0.0.1:8000/docs). En cada operación usa **Try it out** y **Execute**. Después de un login, copia el valor de `access_token` a **Authorize → HTTPBearer**. Si cambias de cuenta, elimina primero la autorización anterior. Mantén el mismo host para que el navegador envíe su cookie.

| Prueba | Pasos y resultado esperado |
| --- | --- |
| Registro | Envía `{"email":"usuario-pruebas@example.com","password":"TU_CLAVE_DE_PRUEBA"}` a `POST /auth/registro` con una contraseña de al menos 12 caracteres. Espera 201 con rol `usuario`. Repite el correo y espera 409. Si agregas `"rol":"admin"` al cuerpo, espera 422. |
| Permisos | Ejecuta `GET /productos/` sin Bearer y espera 401. Haz login como usuario en `POST /auth/login` con `email` y `password`. Autoriza el access y espera 200 en `GET /auth/me` y en productos. Envía `{"nombre":"Categoría prueba equipo"}` a `POST /categorias/` y espera 403. Repite esa creación con el access administrativo y espera 201. Anota el ID. |
| Bloqueo de login | Con una cuenta de prueba distinta, intenta cinco veces una contraseña incorrecta. Luego intenta la correcta y verifica que reciba 401 durante el bloqueo de 15 minutos. |
| Refresh y logout | Inicia sesión. En `POST /auth/refresh` espera 403 sin cabecera. Envía `X-CSRF-Protection: 1` y espera 200. Ejecuta `POST /auth/logout` con la misma cabecera y espera 204. Vuelve a renovar y espera 401. |
| Reutilización de refresh | En un cliente HTTP que permita manejar cookies, guarda la cookie del login y renueva. Conserva también la cookie nueva. Envía la cookie antigua a `POST /auth/refresh` con `X-CSRF-Protection: 1`. Espera 401. Prueba la cookie nueva y espera también 401 porque se revocó la sesión. |
| Recuperación | Inicia sesión como usuario y conserva su access y su cookie. Envía el correo a `POST /auth/recuperacion` y espera 202. Abre [Mailpit](http://127.0.0.1:8025), busca el mensaje y copia su JWT. Envía `{"token":"JWT_DEL_CORREO","nueva_password":"TU_NUEVA_CLAVE_DE_PRUEBA"}` a `POST /auth/restablecer` y espera 204. |
| Validación después del cambio | Repite el restablecimiento y espera 400. Ejecuta `GET /auth/me` con el access anterior y espera 401. Renueva con la cookie anterior y la cabecera de CSRF antes de volver a iniciar sesión y espera 401. Comprueba que el login falle con la contraseña anterior y funcione con la nueva. |
| Persistencia | Ejecuta `docker compose -p cafeteria-pruebas up -d --no-deps --force-recreate --wait web`. Consulta `GET /categorias/{categoria_id}` con el Bearer y el ID anotado. Espera 200 con el mismo registro. |

Si el correo tarda, consulta `docker compose -p cafeteria-pruebas logs --tail 50 web mailpit`. La recuperación responde 202 también para un correo válido que no exista. Un access JWT enviado como token de recuperación devuelve 400.

Cuando termines, usa `docker compose -p cafeteria-pruebas down` para retirar los contenedores y conservar los datos. Si creaste ese entorno exclusivamente para estas pruebas y deseas desechar sus datos, usa `docker compose -p cafeteria-pruebas down --volumes` con el nombre exacto de ese entorno.
