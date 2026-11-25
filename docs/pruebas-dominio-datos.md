# Pruebas de dominio y datos - Entrega III

## Instalación y migraciones

Se configuró un entorno local con Docker Compose y PostgreSQL.

- La base de datos inició correctamente.
- El servicio de migraciones terminó con código 0.
- La revisión actual de Alembic es `71fd6e842b19`.
- `alembic check` no detectó operaciones de actualización pendientes.

## Verificación de seeders

Se ejecutó `seeders.py` dos veces.

| Entidad | Primera ejecución | Segunda ejecución |
|---|---:|---:|
| Categorías | 2 | 2 |
| Clientes | 2 | 2 |
| Productos | 2 | 2 |
| Pedidos | 2 | 2 |

La segunda ejecución omitió la carga porque ya existían datos de negocio.

## Prueba de rollback

Se utilizaron los repositorios de productos y pedidos con `commit=False` dentro de una misma sesión.

Se descontó una unidad de stock, se agregó un pedido y posteriormente se ejecutó `rollback()`.

Se verificó que el stock original y la cantidad de pedidos se conservaron.

Resultado: `ROLLBACK OK: stock y pedidos conservados`.

## Migración con datos previos

Se creó una base de prueba independiente llamada `cafeteria_prueba_migracion`.

Se aplicó la revisión `2a0a434ad066`, se cargaron datos ficticios y se actualizó a la revisión `71fd6e842b19`.

Las cuatro tablas de negocio conservaron sus dos registros cada una. La consulta posterior confirmó que los dos pedidos mantenían relaciones válidas con clientes, productos y categorías.

