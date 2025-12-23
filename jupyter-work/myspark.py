from spark_helper import init_spark

spark=init_spark("My App")

print ("spart version:", spark.version)
print("spark master:", spark.sparkContext.master)