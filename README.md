# taller-databricks-ventas

Desarrollo de un flujo de ventas en Databricks Free Edition mediante una arquitectura Bronze/Silver, un Lakeflow Job y un Lakeflow Spark Declarative Pipeline.

## Objetivo

Almacenar ventas en una tabla Delta, aplicar reglas de calidad, automatizar la carga y transformación, y publicar un resumen por categoría mediante vistas materializadas.

## Estructura

```text
notebooks/          Notebooks para importar en Databricks
databricks-source/  Versiones Python en formato Databricks Source
pipeline/           Definición SQL del pipeline declarativo
docs/               Investigación, guías y resultados esperados
evidencias/         Capturas organizadas por ejercicio
```

## Configuración utilizada

- Catálogo: `workspace`
- Esquema: `ingenieria_datos_juan_nicolas`
- Cómputo: Serverless
- Job: `job_ventas_juan_nicolas`
- Pipeline: `pipeline_ventas_juan_nicolas`

## Orden de ejecución

1. Importar y ejecutar `notebooks/01_cargar_ventas.ipynb`.
2. Consultar Bronze con `notebooks/01b_consultar_ventas.ipynb`.
3. Ejecutar dos veces `notebooks/02_transformar_ventas.ipynb` para comprobar idempotencia.
4. Crear el job con las tareas `cargar_ventas` y `transformar_ventas`.
5. Crear el pipeline con `pipeline/pipeline_ventas.sql`.
6. Ejecutar `notebooks/03_pruebas_pipeline.ipynb` con las acciones `antes`, `agregar` y `despues`.

## Resultados esperados

| Comprobación | Resultado |
|---|---:|
| Registros Bronze | 18 |
| Registros sin duplicados | 17 |
| Registros Silver | 15 |
| Total inicial | 539.000 |
| Aumento de Tecnología | 50.000 |
| Total final del pipeline | 589.000 |

Las capturas del workspace deben corresponder a ejecuciones reales. Consulta `docs/GUIA_ENTREGA.md` para revisar la evidencia requerida.

## Evidencias y validación

El taller fue ejecutado en Databricks por el autor. Se incluyen **15 capturas reales** en el [índice de evidencias](evidencias/README.md), con [resultados comprobados](docs/RESULTADOS_COMPROBADOS.md). Una captura de dependencias se excluyó por mostrar un correo personal; queda pendiente una versión anonimizada.

La revisión local comprueba sintaxis Python, estructura de notebooks, equivalencia de las dos versiones, reglas de limpieza y resultados del SQL mediante una adaptación a SQLite. No ejecuta Spark, Delta ni el planificador de Databricks. Consulta [VALIDACION.md](docs/VALIDACION.md).

El pipeline mostrado usa `Full recompute`. La actualización del resumen está comprobada; no se afirma procesamiento incremental. Tras insertar la venta adicional, Silver conserva 15 filas hasta volver a ejecutar su transformación; la vista del pipeline tiene 16.

## Reproducibilidad

- Importa los `.ipynb` o los `.py` de Databricks Source, no ambos.
- Configura los widgets `catalogo` y `esquema` con permisos de escritura.
- En el job usa `provocar_error=false`; activa `true` únicamente para el fallo controlado y restáuralo después.
- La tarea `transformar_ventas` depende de `cargar_ventas` con `All succeeded`.
- Configura el destino del pipeline en el mismo catálogo y esquema de Bronze. El SQL se ejecuta como fuente del pipeline, no como un notebook independiente.
- Para la venta adicional: pipeline inicial → `accion=antes` → `accion=agregar` → refrescar solo el pipeline → `accion=despues`.
- **La carga sobrescribe Bronze.** No ejecutes la carga ni el job durante la comparación final.

## Documentación

- [Guía de ejecución](docs/GUIA_ENTREGA.md)
- [Guía del job y pipeline](docs/GUIA_JOB_PIPELINE.md)
- [Investigación](docs/INVESTIGACION.md)
- [Resultados esperados](docs/RESULTADOS_ESPERADOS.md)
- [Traspaso y pendientes](TRASPASO_OTRA_CUENTA.md)

## Autor

Juan Nicolás Cortés
