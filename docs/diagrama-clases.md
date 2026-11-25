# Diagrama de clases - Cafetería Universitaria

## Entidades del dominio

```mermaid
classDiagram
    class Categoria 
        {+int id
        +string nombre
        +string descripcion
        +bool estado_activo
        +datetime fecha_creacion}

    class Cliente 
        {+int id
        +string nombre
        +string email
        +string telefono
        +string direccion}

    class Producto 
        {+int id
        +string nombre
        +float precio
        +int stock
        +int categoria_id}

    class Pedido 
       { +int id
        +int cliente_id
        +int producto_id
        +int cantidad
        +float monto_total
        +string estado}

    Categoria "0..1" -- "0..*" Producto : clasifica
    Cliente "0..1" -- "0..*" Pedido : realiza
    Producto "0..1" -- "0..*" Pedido : asociado
```

## Descripción

- Categoria: organiza los productos de la cafetería.
- Cliente: almacena los datos de los compradores.
- Producto: administra los precios y el stock.
- Pedido: registra las compras realizadas.

Las relaciones representan las entidades del dominio.
Las claves foráneas admiten valores nulos en los
modelos revisados, aunque los esquemas de creación
exigen identificadores válidos.