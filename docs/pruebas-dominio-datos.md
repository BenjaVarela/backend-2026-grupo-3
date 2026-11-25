# Pruebas de dominio y datos - Entrega III

## Instalación y migraciones

La comprobación se ejecutó en un proyecto de Docker Compose con un volumen PostgreSQL desechable. Usa la configuración del [README](../README.md#4-inicio-con-docker-compose), puertos disponibles y un nombre de proyecto propio.

En una base de prueba vacía, ejecuta estos comandos.

```powershell
docker compose -p cafeteria-dominio up -d --build --wait
docker compose -p cafeteria-dominio ps -a
docker compose -p cafeteria-dominio exec web python -m alembic current
docker compose -p cafeteria-dominio exec web python -m alembic check
docker compose -p cafeteria-dominio exec web python seeders.py
docker compose -p cafeteria-dominio exec web python seeders.py
```

- La base de datos y la API quedaron saludables.
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

Con los datos de demostración, abre una sesión, elige un producto con stock y cuenta sus pedidos. Actualiza el stock y guarda un pedido mediante los dos repositorios con `commit=False`. Comprueba que el pedido tiene ID y ejecuta `rollback()`. Abre otra sesión y compara el stock y la cantidad de pedidos con los valores iniciales.

Repite el caso con un ID de cliente inexistente. La FK provoca `IntegrityError` en el `flush` de la segunda escritura. Ejecuta `rollback()` y vuelve a comprobar los valores desde otra sesión.

En ambos casos se conservó el stock original y la cantidad de pedidos. También se comprobó que los llamadores que usan los valores por defecto siguen confirmando sus escrituras.

## Lecturas concurrentes de stock

En una sesión de PostgreSQL, lee un producto con `obtener_por_id(id, bloquear=True)` y cambia su stock con `commit=False`. En una segunda sesión, carga primero el mismo producto sin bloqueo y luego solicita la lectura con `bloquear=True`. La segunda lectura debe esperar al primer `commit()` y devolver el stock recién guardado incluso si el objeto ya estaba cargado en esa sesión.

PostgreSQL registró el bloqueo de la segunda sesión y la lectura devolvió el stock actualizado después de confirmar la primera. Esta comprobación cubre el repositorio. El uso del bloqueo y del rollback desde `POST /pedidos/` está descrito en el [traspaso a Diego](dominio-reglas.md#traspaso-a-diego).

## Migración con datos previos

Se creó una base de prueba independiente llamada `cafeteria_prueba_migracion`.

Usa una segunda base nueva dentro del proyecto desechable. Por ejemplo, con el usuario local `postgres`, ejecuta lo siguiente.

```powershell
docker compose -p cafeteria-dominio exec db createdb -U postgres cafeteria_prueba_migracion
docker compose -p cafeteria-dominio exec -e POSTGRES_DB=cafeteria_prueba_migracion web python -m alembic upgrade 2a0a434ad066
docker compose -p cafeteria-dominio exec -e POSTGRES_DB=cafeteria_prueba_migracion web python seeders.py
```

Consulta y registra los valores completos de las cuatro tablas de negocio. Aplica la revisión actual y vuelve a compararlos.

```powershell
docker compose -p cafeteria-dominio exec -e POSTGRES_DB=cafeteria_prueba_migracion web python -m alembic upgrade head
```

Tras actualizar a `71fd6e842b19`, ambas consultas devolvieron las mismas dos filas por tabla con todos sus valores. Los dos pedidos conservaron sus vínculos con clientes y productos, y sus productos conservaron las categorías.
