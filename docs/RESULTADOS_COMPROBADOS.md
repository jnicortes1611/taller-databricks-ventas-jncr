# Resultados comprobados

Las capturas recibidas muestran:

| Comprobación | Resultado |
|---|---:|
| Bronze original | 18 filas |
| Sin duplicados idénticos | 17 filas |
| Silver | 15 filas |
| Alimentos | 101.000 |
| Papeleria | 90.000 |
| Tecnologia inicial | 348.000 |
| Total inicial calculado a partir del resumen | 539.000 |
| Tecnologia después | 398.000 |
| Diferencia | 50.000 |
| Total final calculado a partir del resumen | 589.000 |
| Ventas limpias finales | 16 |

La salida final confirma la aserción de 16 ventas limpias. Las dos capturas de repetición conservan conteos y resumen. Esto respalda la repetibilidad observada, aunque las capturas no comparan cada fila entre ejecuciones.

El job registra éxito inicial, un fallo por `columna_inexistente` (`UNRESOLVED_COLUMN.WITH_SUGGESTION`, SQLSTATE 42703) y éxito final. La etiqueta exacta de la tarea dependiente y sus duraciones individuales no son legibles; no se infieren.

La vista materializada se actualizó después del MERGE de la venta 999. El grafo indica `Full recompute`, por lo que no se afirma ejecución incremental.

Consulta las [capturas originales publicables](../evidencias/README.md). La revisión local se describe en [VALIDACION.md](VALIDACION.md); no constituye una nueva ejecución de Databricks.

La captura final `E4_04_resumen_despues.png` se revisó localmente, pero su publicación quedó bloqueada por revisión automática. Los resultados finales anteriores proceden de esa imagen y no tienen captura final publicada en este repositorio.
