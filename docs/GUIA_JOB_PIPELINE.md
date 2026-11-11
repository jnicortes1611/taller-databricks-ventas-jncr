# Guía de ejecución y evidencias reales

Esta guía prepara los ejercicios 3 y 4. Los estados, duraciones, capturas y resultados del workspace deben registrarse después de ejecutar. El código preparado por sí solo no constituye evidencia de una ejecución en Databricks.

## Preparación única

1. Usar **Databricks Free Edition**, con cómputo **serverless**. Free Edition tiene cuotas de uso; este taller solo necesita dos tareas secuenciales y un pipeline ETL.
2. Importar los notebooks de carga, lectura, transformación y comprobación incluidos en la entrega. Ejecutar la carga con `provocar_error=false` y la transformación antes de crear el pipeline.
3. Anotar el catálogo real y el esquema `ingenieria_datos_tunombre` usados por los notebooks. Comprobar en Catalog Explorer que existe `catalogo.esquema.ventas_bronze`.
4. Utilizar los mismos valores de `catalogo` y `esquema` en cada notebook. No cambiar únicamente el nombre del esquema en la interfaz.

## Ejercicio 3: job de dos tareas

1. Abrir **Jobs & Pipelines** y crear un **Job** llamado `job_ventas_tunombre`. Según la versión del workspace, la creación también puede aparecer bajo **Workflows**.
2. Agregar la tarea **cargar_ventas**, tipo **Notebook**, y seleccionar `01_cargar_ventas`. Usar **Serverless**. Configurar parámetros de notebook (pares clave-valor):

   | Clave | Valor |
   | --- | --- |
   | `catalogo` | Nombre real del catálogo |
   | `esquema` | Esquema real del taller |
   | `provocar_error` | `false` |

3. Agregar **transformar_ventas**, tipo **Notebook**, y seleccionar `02_transformar_ventas`. Usar Serverless y pasar los mismos `catalogo` y `esquema`.
4. En **Depends on**, seleccionar `cargar_ventas`; en **Run if dependencies**, seleccionar **All succeeded**. Guardar. La transformación se ejecutará únicamente después del éxito de la carga.
5. Capturar el grafo con ambas tareas y su dependencia. Ejecutar **Run now**, abrir la ejecución y guardar estados y duraciones reales de ambas tareas.
6. Para el error controlado, editar solo el parámetro de tarea `provocar_error` de **cargar_ventas** a `true`, guardar y ejecutar nuevamente. No crear un parámetro homónimo a nivel job que pueda reemplazarlo. El notebook activará una referencia a columna inexistente antes de sobrescribir Bronze.
7. Abrir la ejecución fallida: capturar el error completo en la salida de `cargar_ventas`, su clase/mensaje y la celda señalada. Capturar también el estado de `transformar_ventas`. Con esta dependencia, la documentación indica el estado **Upstream failed**; registrar el texto que muestre el workspace. La segunda tarea no debe ejecutar la transformación.
8. Restablecer `provocar_error=false`, guardar y ejecutar el job completo mediante **Run now**. Verificar que ambas tareas terminen correctamente. Dejar esta como ejecución final exitosa y capturar sus estados y duraciones.

Texto para completar con los resultados observados:

> En la ejecución [ID/fecha real], activé una referencia a una columna inexistente en la primera tarea. La carga terminó con [mensaje real]. La tarea de transformación quedó en [estado real] porque requería el éxito de la carga. Identifiqué la causa en [celda y detalle real del error]. Restablecí el parámetro y la ejecución [ID/fecha real] finalizó correctamente: carga [duración] y transformación [duración].

## Ejercicio 4: pipeline declarativo

1. Crear un **ETL pipeline** con **Lakeflow Spark Declarative Pipelines**, nombre sugerido `pipeline_ventas_tunombre`. Seleccionar **Serverless** y ejecución disparada/manualmente (**Triggered**, si se muestra), para actualizar cuando se solicite.
2. En **Default location for data assets**, seleccionar el mismo **Catalog** y **Schema** que contienen `ventas_bronze`. Esta configuración también determina dónde se publican las dos vistas materializadas.
3. Agregar `pipeline_ventas.sql` como archivo fuente SQL del pipeline. Si la interfaz solicita crear un notebook SQL, copiar allí el contenido y agregarlo como fuente. No ejecutar estas definiciones como consultas independientes: deben formar parte del pipeline ETL solicitado.
4. Guardar e iniciar una actualización. El código lee `ventas_bronze`, elimina filas idénticas sobre las seis columnas originales, filtra producto vacío/nulo y cantidad/precio no positivos, calcula `total_venta` y agrupa por categoría. Las condiciones `> 0` también excluyen valores nulos.
5. Revisar el grafo: `pipeline_ventas_por_categoria` debe depender de `pipeline_ventas_limpias`, que usa `ventas_bronze`. Capturar el grafo y el estado final. El pipeline calcula las dependencias a partir de las consultas.
6. En Catalog Explorer verificar que ambas vistas están publicadas. Consultar el resumen por categoría **antes** de insertar la nueva venta y guardar sus valores mediante el notebook de comprobación incluido.
7. Agregar la venta de prueba una sola vez mediante el notebook de comprobación. Usar ID nuevo, producto informado, cantidad y precio positivos. Registrar categoría, cantidad, precio y `cantidad × precio`.
8. **No volver a ejecutar `01_cargar_ventas` ni el job de carga durante esta prueba**: la carga vuelve a crear Bronze y eliminaría la venta agregada. Actualizar únicamente el pipeline.
9. Consultar el resumen **después** y compararlo con la instantánea anterior. El total de la categoría de la venta debe subir exactamente por su importe; las otras categorías deben conservar su total. El total general también debe aumentar por ese importe y las ventas limpias por una fila.
10. Guardar captura de la consulta comparativa y de la actualización exitosa. Una materialized view conserva el resultado de la consulta; Databricks decide la estrategia de actualización. El cambio correcto del resultado no demuestra por sí solo que el motor ejecutó un refresco incremental en lugar de un recálculo.

Consulta manual alternativa (sustituir catálogo y esquema):

```sql
SELECT categoria, total_vendido
FROM catalogo.esquema.pipeline_ventas_por_categoria
ORDER BY categoria;
```

## Lista de evidencias que debe contener la entrega

| Evidencia | Qué debe verse |
| --- | --- |
| Job y dependencia | Nombre del job, dos tareas y condición de éxito |
| Primera ejecución exitosa | Estado y duración de cada tarea |
| Ejecución fallida | Error de columna, tarea que falla y estado de la segunda |
| Ejecución corregida | Ambas tareas exitosas con sus duraciones |
| Pipeline | Nombre, vistas y grafo de dependencias |
| Publicación | Catálogo/esquema y ambas vistas materializadas |
| Antes/después | Totales reales, venta insertada y diferencia monetaria |

## Fuentes oficiales verificadas el 6 de noviembre de 2026

- [Free Edition y cómputo serverless](https://docs.databricks.com/aws/en/getting-started/free-edition).
- [Límites de Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).
- [Parámetros de tareas](https://docs.databricks.com/aws/en/jobs/task-parameters).
- [Dependencias y condiciones Run if](https://docs.databricks.com/aws/en/jobs/run-if).
- [Monitorear ejecuciones de Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/monitor).
- [CREATE MATERIALIZED VIEW en pipelines](https://docs.databricks.com/aws/en/ldp/developer/ldp-sql-ref-create-materialized-view).
- [Configurar catálogo y esquema del pipeline](https://docs.databricks.com/aws/en/ldp/target-schema).
- [Vistas materializadas](https://docs.databricks.com/aws/en/ldp/materialized-views).

Las etiquetas de la interfaz pueden variar. Los nombres de parámetros deben coincidir con los widgets de los notebooks importados.
