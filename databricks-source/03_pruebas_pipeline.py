# Databricks notebook source
# MAGIC %md
# MAGIC Configura el catálogo si tu workspace lo requiere. Vacío usa el catálogo actual.
# COMMAND ----------
import re
from pyspark.sql import functions as F

dbutils.widgets.text("catalogo", "")
dbutils.widgets.text("esquema", "ingenieria_datos_juan_nicolas")
catalogo = dbutils.widgets.get("catalogo").strip() or spark.sql("SELECT current_catalog()").first()[0]
esquema = dbutils.widgets.get("esquema").strip()
for etiqueta, identificador in [("catálogo", catalogo), ("esquema", esquema)]:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identificador):
        raise ValueError(f"El {etiqueta} debe contener letras, números o guion bajo y no comenzar por número: {identificador!r}")
def tabla(nombre):
    return f"`{catalogo}`.`{esquema}`.`{nombre}`"
print(f"Catálogo: {catalogo}; esquema: {esquema}")
# COMMAND ----------
# MAGIC %md
# MAGIC ## Secuencia de prueba
# MAGIC 1. Ejecuta el pipeline por primera vez.
# MAGIC 2. Ejecuta este notebook con accion=antes y captura el resumen inicial.
# MAGIC 3. Cambia accion=agregar y ejecuta este notebook. No ejecutes 01_cargar_ventas ni el job.
# MAGIC 4. Ejecuta nuevamente únicamente el pipeline desde su interfaz.
# MAGIC 5. Cambia accion=despues, ejecuta este notebook y captura la comparación.
# MAGIC No repitas accion=antes después de agregar la venta: reemplazaría la referencia inicial.
# COMMAND ----------
dbutils.widgets.dropdown("accion", "antes", ["antes", "agregar", "despues"])
accion = dbutils.widgets.get("accion")
if accion == "antes":
    if spark.table(tabla("ventas_bronze")).filter(F.col("id_venta") == 999).count():
        raise ValueError("La venta 999 ya existe. Restaura Bronze con la carga y refresca el pipeline antes de guardar una nueva referencia inicial.")
    inicial = spark.table(tabla("pipeline_ventas_por_categoria"))
    inicial.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabla("prueba_pipeline_antes"))
    display(spark.table(tabla("prueba_pipeline_antes")).orderBy("categoria"))
    print("Referencia inicial guardada. Siguiente paso: accion=agregar.")
# COMMAND ----------
if accion == "agregar":
    if not spark.catalog.tableExists(f"{catalogo}.{esquema}.prueba_pipeline_antes"):
        raise ValueError("Primero ejecuta accion=antes para guardar la referencia inicial.")
    # La condición por ID hace que repetir esta inserción no duplique la venta.
    spark.sql(f"""
    MERGE INTO {tabla("ventas_bronze")} AS destino
    USING (SELECT 999 AS id_venta, DATE '2026-11-06' AS fecha,
                  'Mouse especial' AS producto, 'Tecnologia' AS categoria,
                  2 AS cantidad, CAST(25000.00 AS DECIMAL(12,2)) AS precio_unitario) AS nueva
    ON destino.id_venta = nueva.id_venta
    WHEN NOT MATCHED THEN INSERT *
    """)
    assert spark.table(tabla("ventas_bronze")).filter(F.col("id_venta") == 999).count() == 1
    print("Venta 999 disponible en Bronze: 2 × 25000 = 50000. Ejecuta ahora el pipeline y luego accion=despues.")
# COMMAND ----------
if accion == "despues":
    antes = spark.table(tabla("prueba_pipeline_antes")).select("categoria", F.col("total_vendido").alias("total_antes"))
    despues = spark.table(tabla("pipeline_ventas_por_categoria")).select("categoria", F.col("total_vendido").alias("total_despues"))
    comparacion = antes.join(despues, "categoria", "full").fillna(0, subset=["total_antes", "total_despues"]).withColumn("diferencia", F.col("total_despues") - F.col("total_antes"))
    display(comparacion.orderBy("categoria"))
    diferencias = {r["categoria"]: r["diferencia"] for r in comparacion.collect()}
    assert diferencias.get("Tecnologia") == 50000, "Refresca el pipeline o revisa la referencia inicial"
    assert all(v == 0 for k, v in diferencias.items() if k != "Tecnologia"), "Cambió una categoría inesperada"
    assert spark.table(tabla("pipeline_ventas_limpias")).count() == 16
    print("Validación correcta: Tecnología aumentó 50000; las otras categorías no cambiaron; hay 16 ventas limpias.")
