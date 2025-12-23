# Spark 3.5 Setup

This is a fresh setup using Spark 3.5 with modern Docker images.

## Quick Start

```bash
# Start all services
docker-compose -f docker-compose-spark35.yml up -d

# Check status
docker-compose -f docker-compose-spark35.yml ps

# View logs
docker-compose -f docker-compose-spark35.yml logs -f
```

## Services

- **Jupyter PySpark**: http://localhost:8888
- **Spark Master UI**: http://localhost:8080
- **Spark Worker UI**: http://localhost:8081
- **HDFS NameNode**: http://localhost:50070
- **Hue (HDFS Browser)**: http://localhost:8088/home

## Usage in Jupyter

```python
from spark_helper import init_spark

# Connect to Spark cluster
spark = init_spark("My App")

# Test
print("Spark version:", spark.version)
print("Spark master:", spark.sparkContext.master)

# Create RDD
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
print(rdd.collect())
```

## Differences from Spark 2.1

- **Spark 3.5** with Adaptive Query Execution
- **Hadoop 3.2.1** (newer version)
- **Java 17** (instead of Java 8)
- **Python 3.11** (instead of Python 3.8)
- **Modern Docker images** (bitnami/spark)
- **Better performance** and features

## Access HDFS

```python
# Read from HDFS
df = spark.read.text("hdfs://namenode:8020/path/to/file")

# Write to HDFS
df.write.text("hdfs://namenode:8020/output/path")
```

