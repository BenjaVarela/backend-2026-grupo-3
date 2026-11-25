# Backend 2026 - Grupo 3

API REST desarrollada para la gestión comercial y transaccional de un sistema de e-commerce e inventario, construida bajo estrictos estándares de arquitectura en capas, patrones de diseño y buenas prácticas de desarrollo backend.

## Integrantes y Responsabilidades

| Integrante | Rol Principal | Responsabilidades |
| :--- | :--- | :--- |
| **Benjamín Varela** *(Líder)* | Coordinación y seguimiento + Documentación e integración | Organización del backlog, seguimiento de hitos, integración de entregables, Swagger/OpenAPI, README y configuración de migraciones Alembic. |
| **Benjamín Riquelme.** | Dominio y datos | Modelado de las 4 entidades ORM, relaciones 1:N, esquemas Pydantic/DTOs, reglas de validación y seeders de carga inicial. |
| **Diego Manquicoy** | API y lógica de negocio | Implementación de la arquitectura por capas, endpoints REST, servicios transaccionales, control ACID y manejo uniforme de errores HTTP. |
| **Mauricio Valdés** | Calidad y pruebas | Verificación funcional de endpoints, colección de pruebas en Swagger, validación de persistencia y consultas con filtro, orden y paginación. |

## 1. Problemática y Alcance

### P1. Situación Concreta
Los administradores y operadores comerciales registran productos, clientes y transacciones de pedidos en planillas desconectadas o sistemas descentralizados, lo que genera inconsistencias en el stock disponible, falta de trazabilidad en las compras y tiempos elevados de auditoría operativa.

### P2. Actores
* **Cliente / Comprador:** Actor que interactúa con el sistema para registrarse y emitir pedidos de compra.
* **Administrador de Inventario / Operador:** Actor encargado de mantener actualizado el catálogo de productos, gestionar categorías y supervisar el estado de los pedidos y el stock.

### P3. Consecuencias
* Venta de productos sin stock físico real debido al desfase en la actualización manual de inventarios.
* Incapacidad para auditar de forma rápida y automatizada el historial transaccional de los clientes.

### P4. Información Administrada
El sistema administra de forma persistente cuatro entidades principales: **Clientes**, **Categorías**, **Productos** y **Pedidos** (con su respectiva relación de detalle/asociación).

### P5. Acciones de la API (Requisitos funcionales)
1. El sistema debe permitir registrar y listar clientes con validación de datos estrictos.
2. El sistema debe permitir gestionar categorías de productos mediante un CRUD completo.
3. El sistema debe permitir administrar el inventario de productos vinculados a categorías.
4. El sistema debe permitir registrar pedidos asociados a clientes específicos.
5. El sistema debe permitir verificar la disponibilidad de stock antes de confirmar cualquier pedido.
6. El sistema debe permitir filtrar, ordenar y paginar catálogos de productos y pedidos.
7. El sistema debe permitir actualizar de manera segura los registros existentes.
8. El sistema debe permitir eliminar registros con respuestas estructuradas en JSON.

### P6. Exclusiones de Alcance
* No incluye pasarela de pagos real ni procesamiento de tarjetas de crédito transaccionales externas.
* No incluye interfaz gráfica de usuario (Frontend web o móvil), limitándose al contrato OpenAPI y pruebas de integración.

### P7. Criterios de Aceptación
* La API responde con códigos de estado HTTP correctos (200, 201, 400, 404, 409, 422).
* Los datos persisten de manera íntegra en la base de datos tras reiniciar la aplicación.
* Las consultas con filtros, ordenamientos y paginación devuelven la estructura de metadatos exacta exigida.

## 2. Tecnologías y Stack Tecnológico

* **Lenguaje:** Python 3.14.10 en la imagen de la API.
* **Framework Web:** FastAPI (con Uvicorn como servidor ASGI)
* **Validación de Datos:** Pydantic (DTOs estrictos)
* **ORM y Base de Datos:** SQLAlchemy y PostgreSQL 15.20.
* **Migraciones de Esquema:** Alembic
* **Pruebas de Contrato:** OpenAPI (Swagger UI)

## 3. Arquitectura por capas

| Responsabilidad | Archivos |
| --- | --- |
| Ensamblaje y configuración | `app/main.py` registra rutas, CORS, errores y salud. `app/config.py` lee el entorno. |
| Presentación | `app/routers/`, `app/schemas/`, `app/dependencies.py` y `app/http_security.py` validan las entradas, resuelven permisos y manejan Bearer, cookies y CSRF. |
| Aplicación | `app/services/` coordina casos de uso. `auth_service.py` administra cuentas, rotación y restablecimiento. `recuperacion.py` coordina el envío del correo tras guardar el permiso. |
| Dominio | `app/domain/auth.py` define roles, políticas y errores. Los modelos ORM de negocio siguen en `app/domain/models.py`. Una cuenta `Usuario` y un perfil comercial `Cliente` son registros independientes. |
| Infraestructura | `app/database.py`, `app/repositories/`, `app/infrastructure/` y `alembic/` se ocupan de persistencia, Argon2id, firma y verificación JWT, SMTP y migraciones. |

En `POST /auth/restablecer`, el router valida el DTO y delega al servicio. El servicio valida el JWT de recuperación, obtiene el usuario a partir de `sub` y bloquea su fila en PostgreSQL. Tras comprobar el `jti`, guarda el nuevo hash, consume el permiso, aumenta la versión de acceso y revoca los refresh en una misma transacción. La siguiente petición Bearer comprueba esa versión contra la guardada en la cuenta.

Los diagramas describen las relaciones de negocio y las cuentas de acceso. [Diagrama de clases](docs/diagrama-clases.md) · [Diagrama de datos](docs/diagrama-datos.md) · [Reglas y validaciones](docs/dominio-reglas.md)

## 4. Inicio con Docker Compose

Se requiere Docker Desktop o Docker Engine con Compose V2. Desde la raíz del repositorio, copia `.env.example` a `.env` (`Copy-Item .env.example .env` en PowerShell o `cp .env.example .env` en Bash). Completa `POSTGRES_PASSWORD` y `JWT_SECRET` con valores distintos. Puedes generar cada valor por separado con `python -c "import secrets; print(secrets.token_urlsafe(48))"` o `openssl rand -hex 32`.

```bash
docker compose up -d --build --wait
docker compose ps -a
```

| Servicio | Acceso local |
| --- | --- |
| API y Swagger | `http://127.0.0.1:8000/docs` |
| Comprobación de disponibilidad | `http://127.0.0.1:8000/health` |
| Adminer | `http://127.0.0.1:8080`. En el formulario selecciona PostgreSQL, servidor `db` y los valores de `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB`. |
| Capturador Mailpit | `http://127.0.0.1:8025`. Recibe el correo SMTP desde la red de Compose. |

Los puertos publicados se pueden cambiar en `.env` mediante `API_PORT`, `ADMINER_PORT` y `MAILPIT_PORT`. PostgreSQL escucha en la red interna de Compose. El volumen `postgres_data` conserva los datos al recrear la API, ejecutar `stop` o ejecutar `down`. Si ya existe un volumen, utiliza su usuario, contraseña y base de datos. PostgreSQL aplica esas variables de inicialización solo al crear un volumen vacío.

| Operación | Comando |
| --- | --- |
| Construir la imagen | `docker compose build migrate` |
| Iniciar o actualizar | `docker compose up -d --build --wait` |
| Aplicar migraciones manualmente | `docker compose run --rm migrate` |
| Consultar la revisión de la base | `docker compose exec web python -m alembic current` |
| Cargar datos de demostración en una base de negocio vacía | `docker compose exec web python seeders.py` |
| Crear una cuenta administrativa | `docker compose exec web python -m app.crear_admin admin@example.com` |
| Consultar logs | `docker compose logs -f web migrate db mailpit` |
| Detener o retirar los contenedores | `docker compose stop` o `docker compose down` |

El servicio `migrate` ejecuta Alembic después del chequeo de PostgreSQL y la API arranca cuando la migración termina correctamente. El comando administrativo solicita la contraseña sin mostrarla y requiere un correo nuevo. Usa correos de demostración válidos. Mantén Adminer y Mailpit en la interfaz local.

Al ejecutar la API fuera de Compose, configura `DATABASE_URL` o las variables `POSTGRES_*`. Con HTTPS deja `COOKIE_SECURE=true` y configura `APP_ORIGINS` con orígenes exactos, separados por comas. Para un servidor de correo real, configura `SMTP_HOST`, `SMTP_PORT`, `SMTP_FROM` y, según el proveedor, `SMTP_USERNAME`, `SMTP_PASSWORD` y `SMTP_TLS=starttls` o `ssl`.

## 5. Contrato OpenAPI y flujos de autenticación

| Operación | Autorización |
| --- | --- |
| Lectura de categorías y productos | Access Bearer de `usuario` o `admin` |
| Crear, actualizar o eliminar categorías y productos | Access Bearer de `admin` |
| Consultar o gestionar clientes y pedidos | Access Bearer de `admin` |

Swagger muestra el Bearer y los errores 401 y 403 de las operaciones protegidas. Las consultas de productos conservan filtros, orden y paginación.

| Ruta | Entrada y resultado |
| --- | --- |
| `POST /auth/registro` | JSON con `email` y `password`. Crea una cuenta `usuario` y responde 201. Un correo duplicado devuelve 409. |
| `POST /auth/login` | JSON con `email` y `password`. Devuelve el access y establece la cookie refresh. Tras cinco intentos fallidos consecutivos se bloquea temporalmente el login durante 15 minutos. |
| `GET /auth/me` | Devuelve el usuario y su rol para un Bearer válido. |
| `POST /auth/refresh` | Envía la cookie y `X-CSRF-Protection: 1`. Entrega otro access y rota la cookie. |
| `POST /auth/logout` | Envía la cookie y `X-CSRF-Protection: 1`. Revoca la familia de refresh, borra la cookie y responde 204. |
| `POST /auth/recuperacion` | JSON con `email`. Responde 202 con el mismo mensaje para cualquier correo válido. Se permite un envío por minuto por cuenta. |
| `POST /auth/restablecer` | JSON con `token` y `nueva_password`. Cambia la contraseña y responde 204. |

El access JWT dura 15 minutos. El refresh es opaco y se guarda como hash. La familia dura como máximo siete días desde el login y se revoca si se reutiliza un refresh rotado. Tras el logout, un access emitido conserva su ventana de validez. La cookie es HttpOnly, queda limitada a `/auth` y usa `SameSite=Lax` para el flujo de navegador del mismo sitio. Refresh y logout requieren una cabecera personalizada y verifican el origen cuando el navegador lo envía. En HTTPS se añade `Secure`.

Para demostrar la recuperación, registra una cuenta de prueba, inicia sesión y solicita la recuperación. Abre Mailpit y copia el JWT del correo a `POST /auth/restablecer`. El JWT de recuperación expira en diez minutos y cada cuenta tiene un único permiso vigente. Al cambiar la contraseña se invalidan ese permiso, las solicitudes anteriores y todos los access y refresh previos. Registro y restablecimiento usan la misma política de 12 a 128 caracteres y almacenan un hash Argon2id.

## 6. Pruebas Iniciales y Evidencias

1. **Creación exitosa** de recursos con códigos 201.
2. **Validación fallida** (Retorno de error 422 por tipos o longitudes incorrectas).
3. **Recurso no encontrado** (Retorno de error 404 estructurado).
4. **Regla de negocio** (Validación de stock insuficiente con error controlado).
5. **Consulta avanzada** mediante filtros, ordenamiento (`asc`/`desc`) y paginación con metadatos exactos (`items`, `total`, `pagina`, `limite`, `total_paginas`).
6. **Persistencia** comprobada tras reiniciar el servicio de Uvicorn.
