"""
Helper module for connecting to Spark 3.5 cluster and HDFS
"""
import os

def init_spark(app_name="PySpark Notebook", master="spark://spark-master:7077"):
    """
    Initialize and return a SparkSession connected to the cluster
    
    Args:
        app_name: Name of the Spark application
        master: Spark master URL (default: spark://spark-master:7077)
    
    Returns:
        SparkSession instance
    """
    from pyspark.sql import SparkSession
    
    import sys
    python_exec = sys.executable
    
    spark = SparkSession.builder \
        .appName(app_name) \
        .master(master) \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
        .config("spark.pyspark.python", python_exec) \
        .config("spark.pyspark.driver.python", python_exec) \
        .config("spark.driver.host", "jupyter-pyspark") \
        .config("spark.driver.bindAddress", "0.0.0.0") \
        .getOrCreate()
    
    return spark

def get_spark_context(spark):
    """
    Get SparkContext from SparkSession
    
    Args:
        spark: SparkSession instance
    
    Returns:
        SparkContext instance
    """
    return spark.sparkContext
