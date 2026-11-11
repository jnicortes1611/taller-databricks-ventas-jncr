# Resultados calculados del ejemplo

Son valores calculados localmente a partir de los datos incluidos. No sustituyen las salidas ni las capturas de Databricks.

| Etapa | Filas |
|---|---:|
| ventas_bronze original | 18 |
| Después de eliminar la copia idéntica | 17 |
| ventas_silver después de descartar las dos ventas inválidas | 15 |
| pipeline_ventas_limpias después de insertar la venta 999 y actualizar | 16 |

| Categoría | Total inicial | Después de la venta 999 | Diferencia |
|---|---:|---:|---:|
| Alimentos | 101.000,00 | 101.000,00 | 0,00 |
| Papeleria | 90.000,00 | 90.000,00 | 0,00 |
| Tecnologia | 348.000,00 | 398.000,00 | 50.000,00 |
| Total | 539.000,00 | 589.000,00 | 50.000,00 |

La venta 999 corresponde a dos unidades de 25.000,00 en Tecnologia. Si la comparación muestra otra diferencia, revisa que se haya actualizado el pipeline, que la referencia inicial se guardara antes de insertar y que no se ejecutara la carga durante la prueba.

Después de la venta adicional, Silver permanece en su estado anterior porque no se vuelve a ejecutar la transformación: el ejercicio final compara las vistas del pipeline, no exige actualizar Silver.
