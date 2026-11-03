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
* No incluye autenticación avanzada por tokens JWT ni roles de seguridad avanzados (foco exclusivo en la lógica de negocio y persistencia).
* No incluye interfaz gráfica de usuario (Frontend web o móvil), limitándose al contrato OpenAPI y pruebas de integración.

### P7. Criterios de Aceptación
* La API responde con códigos de estado HTTP correctos (200, 201, 400, 404, 409, 422).
* Los datos persisten de manera íntegra en la base de datos tras reiniciar la aplicación.
* Las consultas con filtros, ordenamientos y paginación devuelven la estructura de metadatos exacta exigida.

## 2. Tecnologías y Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI (con Uvicorn como servidor ASGI)
* **Validación de Datos:** Pydantic (DTOs estrictos)
* **ORM y Base de Datos:** SQLAlchemy y SQLite (preparado para PostgreSQL)
* **Migraciones de Esquema:** Alembic
* **Pruebas de Contrato:** OpenAPI (Swagger UI)

## 3. Arquitectura por Capas y Organización del Código

El proyecto sigue una estricta **Arquitectura en Capas** para garantizar la separación de responsabilidades (SoC):

```text
app/
├── main.py                     # Ensamblaje principal de la aplicación FastAPI y manejo de excepciones
├── database.py                 # Configuración del engine, SessionLocal y dependencias de BD (yield/close)
├── domain/
│   └── models.py               # Entidades del dominio y modelos ORM de SQLAlchemy
├── schemas/                    # DTOs de Pydantic para validación de entrada y serialización de salida
│   ├── categoria.py
│   ├── cliente.py
│   ├── pedido.py
│   └── producto.py
├── repositories/               # Capa de persistencia y consultas aisladas al ORM
│   ├── categorias_repository.py
│   ├── clientes_repository.py
│   ├── pedidos_repository.py
│   └── productos_repository.py
├── services/                   # Lógica de negocio transaccional y control ACID
│   └── pedido_service.py
└── routers/                    # Capa de presentación (Endpoints HTTP RESTful)
    ├── categorias.py
    ├── clientes.py
    ├── pedidos.py
    └── productos.py
```

### Recorrido de una Solicitud (Request Flow)
1. **Cliente HTTP:** Envía la petición estructurada en formato JSON.
2. **Capa de Presentación (`routers/`):** Intercepta la petición, valida la estructura mediante **DTOs de Pydantic** y delega la ejecución inyectando la sesión de base de datos (`Depends`).
3. **Capa de Lógica de Negocio (`services/`):** Ejecuta las reglas de dominio y maneja la transacción atómica (`commit` / `rollback`).
4. **Capa de Acceso a Datos (`repositories/`):** Traduce las operaciones a comandos del **ORM SQLAlchemy**.
5. **Capa de Persistencia (`database.db`):** Almacena y consolida la información de manera permanente.

## 4. Guía de Instalación y Ejecución Local

Sigue estos pasos para clonar, configurar y poner en marcha el proyecto desde una copia limpia:

### 1. Clonar el repositorio
```bash
git clone <URL-DEL-REPOSITORIO>
cd backend-2026-grupo-3
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
# En Windows (Git Bash / CMD):
source venv/Scripts/activate
# En Linux / macOS:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` basado en el archivo de ejemplo (si aplica) o verifica que la URL por defecto de la base de datos en `app/database.py` esté activa.

### 5. Aplicar migraciones con Alembic
```bash
alembic upgrade head
```

### 6. Ejecutar seeders (Carga inicial de datos)
Para poblar la base de datos con los registros iniciales obligatorios:
```bash
python seeders.py
```

### 7. Iniciar el servidor de desarrollo
```bash
uvicorn app.main:app --reload
```
La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

## 5. Contrato OpenAPI y Endpoints Principales

La API cuenta con un CRUD completo para las entidades principales y cumple con los 12 endpoints funcionales mínimos exigidos:
* `/clientes` (GET, POST, GET /{id}, PUT /{id}, DELETE /{id})
* `/categorias` (GET, POST, GET /{id}, PUT /{id}, DELETE /{id})
* `/productos` (GET, POST, GET /{id}, PUT /{id}, DELETE /{id}) [Soporta filtrado, ordenamiento y paginación en un mismo GET].
* `/pedidos` (GET, POST, GET /{id}, DELETE /{id})

## 6. Pruebas Iniciales y Evidencias

1. **Creación exitosa** de recursos con códigos 201.
2. **Validación fallida** (Retorno de error 422 por tipos o longitudes incorrectas).
3. **Recurso no encontrado** (Retorno de error 404 estructurado).
4. **Regla de negocio** (Validación de stock insuficiente con error controlado).
5. **Consulta avanzada** mediante filtros, ordenamiento (`asc`/`desc`) y paginación con metadatos exactos (`items`, `total`, `pagina`, `limite`, `total_paginas`).
6. **Persistencia** comprobada tras reiniciar el servicio de Uvicorn.