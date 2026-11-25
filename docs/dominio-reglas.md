# Entidades, reglas y validaciones

Los modelos viven en [app/domain/models.py](../app/domain/models.py). Las relaciones y columnas están en los [diagramas de clases](diagrama-clases.md) y [datos](diagrama-datos.md).

| Entidad | Atributos además del ID | Restricciones y relaciones |
| --- | --- | --- |
| Categoría | Nombre, descripción, estado activo, fecha de creación | Nombre obligatorio y único. Una categoría puede clasificar varios productos. |
| Cliente | Nombre, correo, teléfono, dirección | Nombre y correo obligatorios. Correo único en la base. Un cliente puede realizar varios pedidos. |
| Producto | Nombre, precio, stock, categoría | Nombre, precio y stock obligatorios en la base. El DTO comprueba precio positivo y stock no negativo. Un producto puede aparecer en varios pedidos. |
| Pedido | Cliente, producto, cantidad, monto total, estado | Cantidad, total y estado obligatorios en la base. Las FK de negocio admiten nulos, mientras que los DTO de creación exigen identificadores positivos. |

La persistencia de cuentas y sesiones está en [app/infrastructure/auth_models.py](../app/infrastructure/auth_models.py). La cuenta `Usuario` es independiente del cliente de negocio.

## Reglas de negocio comprobables

| Regla | Dónde se aplica | Estado |
| --- | --- | --- |
| Una compra requiere stock suficiente. | [Servicio de pedidos](../app/services/pedido_service.py) | Devuelve 409 cuando la cantidad supera el stock leído. La protección ante concurrencia requiere usar la lectura con bloqueo en el servicio. |
| El servidor calcula el total del pedido a partir del precio y la cantidad. | [Servicio de pedidos](../app/services/pedido_service.py) | Implementada. |
| Todo pedido nuevo queda pendiente. | [Servicio de pedidos](../app/services/pedido_service.py) | Implementada. |
| Descontar stock y guardar el pedido requiere una sola transacción. | [Repositorio de productos](../app/repositories/productos_repository.py) y [repositorio de pedidos](../app/repositories/pedidos_repository.py) | Los repositorios admiten revertir las dos escrituras juntas. Falta conectar ese flujo al servicio de pedidos. |

## Seis tipos de validación

| Tipo | Caso concreto | Dónde se comprueba |
| --- | --- | --- |
| Longitud | Nombre de categoría entre 3 y 50 caracteres. | [DTO de categoría](../app/schemas/categoria.py) |
| Numérica | Cantidad de pedido entre 1 y 100. | [DTO de pedido](../app/schemas/pedido.py) |
| Valores permitidos | Estado pendiente, pagado, entregado o cancelado. | [Enum de pedido](../app/schemas/pedido.py) |
| Formato | Dirección de correo del cliente válida. | [DTO de cliente](../app/schemas/cliente.py) |
| Existencia relacionada | El cliente y el producto del pedido deben existir. | [Servicio de pedidos](../app/services/pedido_service.py) |
| Regla de negocio | La cantidad no puede superar el stock disponible. | [Servicio de pedidos](../app/services/pedido_service.py) |
