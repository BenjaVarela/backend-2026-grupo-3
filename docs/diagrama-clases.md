# Diagrama de clases de la Cafetería Universitaria

```mermaid
classDiagram
    class Categoria {
        +int id
        +string nombre
        +string descripcion
        +bool estado_activo
        +datetime fecha_creacion
    }
    class Cliente {
        +int id
        +string nombre
        +string email
        +string telefono
        +string direccion
    }
    class Producto {
        +int id
        +string nombre
        +float precio
        +int stock
        +int categoria_id
    }
    class Pedido {
        +int id
        +int cliente_id
        +int producto_id
        +int cantidad
        +float monto_total
        +string estado
    }
    class Usuario {
        +int id
        +string email
        +string rol
        +bool activo
    }
    class RefreshToken {
        +string token_hash
        +int usuario_id
        +int expira
        +bool revocado
    }
    Categoria "0..1" -- "0..*" Producto : clasifica
    Cliente "0..1" -- "0..*" Pedido : realiza
    Producto "0..1" -- "0..*" Pedido : asociado
    Usuario "1" -- "0..*" RefreshToken : posee
```

`Cliente` identifica a un comprador y `Usuario` a una cuenta de acceso independiente. Las claves foráneas de negocio admiten valores nulos en PostgreSQL. Los DTO de creación exigen identificadores válidos. Las clases de autenticación muestran sus atributos principales. El [diagrama de datos](diagrama-datos.md) incluye todas las columnas.
