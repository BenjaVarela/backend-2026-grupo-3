# Diagrama de datos de la Cafetería Universitaria

```mermaid
erDiagram
    CATEGORIAS |o--o{ PRODUCTOS : clasifica
    CLIENTES |o--o{ PEDIDOS : realiza
    PRODUCTOS |o--o{ PEDIDOS : contiene
    USUARIOS ||--o{ REFRESH_TOKENS : posee

    CATEGORIAS {
        int id PK
        varchar nombre UK
        varchar descripcion
        boolean estado_activo
        timestamp fecha_creacion
    }
    CLIENTES {
        int id PK
        varchar nombre
        varchar email UK
        varchar telefono
        varchar direccion
    }
    PRODUCTOS {
        int id PK
        varchar nombre
        double precio
        int stock
        int categoria_id FK
    }
    PEDIDOS {
        int id PK
        int cliente_id FK
        int producto_id FK
        int cantidad
        double monto_total
        varchar estado
    }
    USUARIOS {
        int id PK
        varchar email UK
        varchar password_hash
        varchar rol
        boolean activo
        int version_acceso
        int intentos_fallidos
        bigint bloqueo_hasta
        bigint reset_disponible_desde
        varchar reset_jti
    }
    REFRESH_TOKENS {
        varchar token_hash PK
        int usuario_id FK
        varchar familia
        bigint expira
        boolean rotado
        boolean revocado
    }
```

PK identifica la clave primaria, FK la clave foránea y UK una columna única. Las claves foráneas de negocio admiten valores nulos. Cada refresh requiere un usuario y se elimina en cascada al eliminar la cuenta. El correo de acceso es único en `usuarios` y el rol admite `usuario` o `admin`. `usuarios` y `clientes` almacenan registros independientes.
