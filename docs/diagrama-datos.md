# Diagrama de datos - Cafetería Universitaria

## Modelo entidad-relación

```mermaid
erDiagram
    CATEGORIAS |o--o{ PRODUCTOS : clasifica
    CLIENTES |o--o{ PEDIDOS : realiza
    PRODUCTOS |o--o{ PEDIDOS : contiene

    CATEGORIAS 
        {int id PK
        varchar nombre UK
        varchar descripcion
        boolean estado_activo
        datetime fecha_creacion}

    CLIENTES 
        {int id PK
        varchar nombre
        varchar email UK
        varchar telefono
        varchar direccion}

    PRODUCTOS 
        {int id PK
        varchar nombre
        float precio
        int stock
        int categoria_id FK}

    PEDIDOS 
        {int id PK
        int cliente_id FK
        int producto_id FK
        int cantidad
        float monto_total
        varchar estado}
```

## Claves y relaciones

- PK: clave primaria.
- FK: clave foránea.
- UK: clave única.

## Integridad de los datos

- Las categorías se relacionan con los productos.
- Los clientes se relacionan con los pedidos.
- Los productos se relacionan con los pedidos.
- El nombre de la categoría y el correo del cliente son únicos.
- Las migraciones se administran mediante Alembic.
- Los repositorios permiten controlar las transacciones.
- Las pruebas realizadas verificaron el rollback y la
  conservación de registros durante la última migración.

## Alcance

Este diagrama representa las cuatro tablas de negocio.
Las tablas de autenticación quedan fuera de este diagrama.