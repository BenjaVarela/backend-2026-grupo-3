# Sistema de Gestión de Pedidos - Cafetería Universitaria
**Curso:** ICINF1108 Desarrollo de Backend  
**Institución:** Universidad Católica de Temuco  
**Grupo:** Grupo 3  

---

## Integrantes y Responsabilidades

| Integrante | Rol Principal | Responsabilidades |
| :--- | :--- | :--- |
| **Benjamín Varela** *(Líder)* | Coordinación y seguimiento + Documentación e integración | Organización del backlog, seguimiento de hitos, integración de entregables, Swagger/OpenAPI y coherencia general del proyecto. |
| **Benjamín Riquelme.** | Dominio y datos | Modelado de las 4 entidades, relaciones 1:N, esquemas Pydantic/DTOs y reglas de validación. |
| **Diego Manquicoy** | API y lógica de negocio | Implementación de carpetas, endpoints, servicios, controladores, reglas de negocio y manejo de errores HTTP. |
| **Mauricio Valdés** | Calidad y pruebas | Verificación funcional de endpoints, colección de pruebas en Postman, validación de errores y filtro/orden/paginación. |

---

## Problemática y Alcance (P1 - P7)

### P1. Situación actual
La cafetería universitaria registra actualmente las órdenes de comida y bebidas de forma manual en comandas de papel y planillas desvinculadas durante los horarios de mayor flujo. Esto genera cuellos de botella en la atención, falta de visibilidad del inventario en tiempo real y errores al despachar los productos.

### P2. Actores que experimentan el problema
* **Clientes (Estudiantes y Docentes):** Experimentan largas filas y frustración al solicitar productos que ya se han agotado.
* **Cajeros y Personal de Cocina:** Presentan dificultades para coordinar la preparación de las órdenes, provocando confusión en los estados de entrega y descuadres de stock.

### P3. Consecuencias observables
* **Retrasos significativos en la entrega de pedidos** durante los recesos entre clases.
* **Pérdida de insumos y ventas no concretadas** por falta de control sobre el stock real de cada producto.

### P4. Información que administrará el sistema
El backend administrará 4 entidades en memoria con relaciones Uno a Muchos (1:N):
* **`Cliente`:** `id`, `nombre`, `correo`, `telefono`, `tipo_cliente`
* **`CategoriaProducto`:** `id`, `nombre`, `descripcion`, `activa`
* **`Producto`:** `id`, `nombre`, `precio`, `stock`, `id_categoria` *(Relación 1:N con CategoriaProducto)*
* **`Pedido`:** `id`, `id_cliente`, `id_producto`, `cantidad`, `monto_total`, `estado` *(Relación 1:N con Cliente)*

### P5. Acciones que debe permitir la API
1. El sistema debe permitir registrar nuevos productos asociados a una categoría.
2. El sistema debe permitir consultar el catálogo completo de productos con filtrado, ordenamiento y paginación.
3. El sistema debe permitir actualizar los datos y stock de un producto existente.
4. El sistema debe permitir eliminar un producto del menú.
5. El sistema debe permitir registrar nuevos clientes en la plataforma.
6. El sistema debe permitir consultar la información y lista de pedidos de un cliente específico por ID.
7. El sistema debe permitir crear un nuevo pedido calculando el monto total y descontando el stock del producto.
8. El sistema debe permitir actualizar el estado de un pedido (`pendiente`, `en_preparacion`, `listo`, `entregado`).
9. El sistema debe permitir listar todos los pedidos filtrados por su estado actual.
10. El sistema debe permitir registrar y listar las categorías de productos disponibles.

### P6. Exclusiones de alcance
1. No se incluirá una interfaz gráfica de usuario (Frontend); las pruebas se realizarán mediante la documentación Swagger/OpenAPI o Postman.
2. No se integrará una base de datos relacional externa ni persistencia en disco (almacenamiento en memoria mediante listas o diccionarios).
3. No se implementará autenticación de usuarios ni integración con pasarelas de pago reales para esta entrega.

### P7. Criterios de aceptación
1. La API ejecuta las operaciones CRUD completas para la entidad `Producto` respondiendo con códigos HTTP apropiados (200, 201, 204, 404).
2. La API rechaza la creación de un pedido si la cantidad solicitada supera el stock disponible del producto, retornando un código HTTP `400 Bad Request` o `409 Conflict` con formato JSON estándar de error.
3. El endpoint GET de la colección de productos permite filtrar por categoría, ordenar por precio y paginar (`pagina` y `limite`) devolviendo los metadatos correspondientes (`total`, `total_paginas`).
4. La API valida datos de entrada rechazando entradas inválidas (textos vacíos, números negativos, correo inválido) con estado HTTP `422 Unprocessable Entity`.
5. Permite consultar la lista completa de pedidos asociados a un cliente mediante la relación Uno a Muchos.

---

## Contrato de la API (REST)

| Método | Endpoint | DTO Entrada | DTO Salida | Código Estado | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/productos` | `ProductoCreate` | `ProductoResponse` | `201 Created` | Registra un nuevo producto en el sistema. |
| `GET` | `/productos` | N/A | `List[ProductoResponse]` | `200 OK` | Consulta la colección con filtro, ordenamiento y paginación. |
| `GET` | `/productos/{id}` | N/A | `ProductoResponse` | `200 OK` / `404` | Obtiene el detalle de un producto por su ID. |
| `PUT` | `/productos/{id}` | `ProductoUpdate` | `ProductoResponse` | `200 OK` / `404` | Actualiza datos o stock de un producto. |
| `DELETE` | `/productos/{id}` | N/A | N/A | `204 No Content` | Elimina un producto del catálogo. |
| `POST` | `/clientes` | `ClienteCreate` | `ClienteResponse` | `201 Created` | Registra un nuevo cliente. |
| `GET` | `/clientes/{id}` | N/A | `ClienteResponse` | `200 OK` / `404` | Consulta un cliente por su ID. |
| `GET` | `/clientes/{id}/pedidos`| N/A | `List[PedidoResponse]` | `200 OK` / `404` | Lista los pedidos de un cliente específico. |
| `POST` | `/pedidos` | `PedidoCreate` | `PedidoResponse` | `201 Created` / `400`| Crea un pedido, calcula el total y descuenta stock. |
| `GET` | `/pedidos` | N/A | `List[PedidoResponse]` | `200 OK` | Lista todos los pedidos con filtro opcional por estado. |
| `PATCH`| `/pedidos/{id}/estado` | `EstadoPedido` | `PedidoResponse` | `200 OK` / `404` | Actualiza el estado de un pedido. |
| `GET` | `/categorias` | N/A | `List[CategoriaResponse]`| `200 OK` | Lista las categorías disponibles. |

---

## Estructura del Proyecto

```text
app/
├── domain/
├── repositories/
├── routers/
├── schemas/
├── services/
└── main.py
