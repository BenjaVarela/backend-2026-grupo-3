# Entidades y reglas de negocio

## Entidades del sistema

### Categoria
- Identificador único.
- Nombre obligatorio y único.
- Descripción opcional.
- Estado activo.
- Fecha de creación.
- Relación con los productos.

### Cliente
- Identificador único.
- Nombre obligatorio.
- Correo electrónico válido y único.
- Teléfono y dirección opcionales.
- Relación con los pedidos.

### Producto
- Identificador único.
- Nombre obligatorio.
- Precio mayor que cero.
- Stock mayor o igual a cero.
- Identificador de la categoría asociada.

### Pedido
- Identificador único.
- Identificador del cliente.
- Identificador del producto.
- Cantidad entre 1 y 100 unidades.
- Monto total.
- Estado del pedido.

## Relaciones entre entidades

- Una categoría puede tener varios productos.
- Un cliente puede tener varios pedidos.
- Un producto puede estar asociado a varios pedidos.

## Reglas de negocio

1. El cliente debe existir antes de realizar un pedido.
2. El producto solicitado debe existir.
3. El stock debe ser suficiente para realizar el pedido.
4. El monto total se calcula multiplicando el precio
   del producto por la cantidad solicitada.
5. Los pedidos nuevos comienzan en estado pendiente.
6. Los estados válidos son pendiente, pagado,
   entregado y cancelado.
7. El descuento de stock y la creación del pedido
   deben ejecutarse dentro de una misma transacción.
8. Si falla la transacción, se deben revertir los cambios.

## Control de transacciones

Los repositorios permiten utilizar commit=False para
controlar la transacción desde el servicio de pedidos.

La prueba de rollback confirmó que se conserva el stock
original y la cantidad de pedidos al revertir la sesión.

