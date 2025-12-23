# Jupyter PySpark Notebook

This directory contains your Jupyter notebooks with PySpark support.

## Accessing the Notebook

1. Start the services: `docker-compose up -d`
2. Access Jupyter at: `http://localhost:8888`
3. The notebook has no password/token for easy access

## Connecting to Spark Cluster

Use this code in your notebook to connect to the Spark cluster:

```python
from spark_helper import init_spark

# Initialize Spark connection
spark = init_spark("My App")

# Or manually:
import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("My App") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
    .getOrCreate()

# Test connection
print("Spark version:", spark.version)
print("Spark master:", spark.sparkContext.master)
```

## Accessing HDFS

### Using Spark APIs

```python
from spark_helper import init_spark

spark = init_spark("HDFS Access")

# Read from HDFS
df = spark.read.text("hdfs://namenode:8020/path/to/file")

# Write to HDFS
df.write.text("hdfs://namenode:8020/output/path")
```

### Using Filesystem-like Interface

```python
from hdfs_filesystem import HDFSPath

# Create a file path (like pathlib.Path)
file_path = HDFSPath("/my-data/test.txt")

# Write to file (like open().write())
file_path.write_text("Hello from HDFS!")

# Read from file (like open().read())
content = file_path.read_text()
print(content)

# Check if exists (like os.path.exists())
print(file_path.exists())
print(file_path.is_file())
print(f"Size: {file_path.size()} bytes")

# List directory (like os.listdir())
root = HDFSPath("/")
for item in root.listdir():
    print(item)

# Create directory (like os.mkdir())
new_dir = HDFSPath("/my-directory")
new_dir.mkdir()
```

## Available Services

- **Jupyter (PySpark)**: http://localhost:8888
- **Spark Notebook (Scala)**: http://localhost:9001
- **Spark Master UI**: http://localhost:8080
- **HDFS NameNode**: http://localhost:50070
- **Hue (HDFS Browser)**: http://localhost:8088/home

