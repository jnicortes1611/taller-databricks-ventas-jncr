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
# MAGIC ## Limpieza y resumen
# MAGIC Se eliminan duplicados idénticos y registros inválidos. Overwrite evita acumular filas al repetir el proceso.
# COMMAND ----------
bronze = spark.table(tabla("ventas_bronze"))
sin_duplicados = bronze.dropDuplicates()
limpias = sin_duplicados.filter(
    F.col("producto").isNotNull()
    & (F.length(F.trim(F.col("producto"))) > 0)
    & (F.col("cantidad") > 0)
    & (F.col("precio_unitario") > 0)
).withColumn("total_venta", (F.col("cantidad") * F.col("precio_unitario")).cast("decimal(20,2)"))
resumen = limpias.groupBy("categoria").agg(F.sum("total_venta").alias("total_vendido"))
conteos = [("Bronze", bronze.count()), ("Sin duplicados", sin_duplicados.count()), ("Silver", limpias.count())]
display(spark.createDataFrame(conteos, ["etapa", "registros"]))
limpias.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabla("ventas_silver"))
resumen.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabla("ventas_por_categoria"))
# COMMAND ----------
silver = spark.table(tabla("ventas_silver"))
assert silver.count() == silver.dropDuplicates().count(), "Hay duplicados en Silver"
assert silver.filter(F.col("producto").isNull() | (F.length(F.trim("producto")) == 0) | (F.col("cantidad") <= 0) | (F.col("precio_unitario") <= 0)).count() == 0
assert silver.agg(F.sum("total_venta")).first()[0] == spark.table(tabla("ventas_por_categoria")).agg(F.sum("total_vendido")).first()[0]
display(spark.table(tabla("ventas_por_categoria")).orderBy("categoria"))
print("Con los datos originales: 18 → 17 → 15. Total vendido: 539000.00")
# COMMAND ----------
# MAGIC %md
# MAGIC Ejecuta este notebook otra vez y captura los conteos y el resumen: deben ser idénticos mientras Bronze no cambie.
