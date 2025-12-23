# Hadoop Spark Cluster - Spark 3.5 Setup

A complete Docker Compose setup for running Apache Spark 3.5.7 cluster with HDFS, Jupyter Notebook, and PySpark support.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/gusti-andika/hadoop-spark-cluster.git
cd hadoop-spark-cluster

# Start all services
docker-compose -f docker-compose-spark35.yml up -d

# Check status
docker-compose -f docker-compose-spark35.yml ps

# View logs
docker-compose -f docker-compose-spark35.yml logs -f
```

## 📦 Services

| Service | URL | Description |
|---------|-----|-------------|
| **Jupyter PySpark** | http://localhost:8888 | Interactive Python notebooks with PySpark |
| **Spark Master UI** | http://localhost:8080 | Spark cluster monitoring and job tracking |
| **Spark Worker UI** | http://localhost:8081 | Worker node status and metrics |
| **HDFS NameNode UI** | http://localhost:50070 | HDFS filesystem browser |
| **Hue (HDFS Browser)** | http://localhost:8088 | User-friendly HDFS file browser |

## 🛠️ Technology Stack

- **Spark**: 3.5.7 (Official Docker image)
- **Hadoop**: 2.8 (HDFS for distributed storage)
- **Python**: 3.10 (PySpark 3.5.7)
- **Java**: 17 (Required for Spark 3.5)
- **Jupyter**: scipy-notebook with PySpark support

## 📝 Usage in Jupyter

### Basic Spark Operations

```python
from spark_helper import init_spark

# Initialize Spark session
spark = init_spark("My Application")

# Check Spark version
print("Spark version:", spark.version)
print("Spark master:", spark.sparkContext.master)

# Create RDD
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
print("RDD sum:", rdd.sum())
print("RDD count:", rdd.count())
```

### Working with DataFrames

```python
# Create DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

# Perform operations
df.filter(df.age > 28).show()
df.groupBy("age").count().show()
```

### Accessing HDFS

```python
# Read from HDFS
df = spark.read.csv("hdfs://namenode:8020/data/sales/customers/*", 
                    header=False, inferSchema=True)
df.show()

# Write to HDFS
df.write.mode("overwrite").csv("hdfs://namenode:8020/output/results")
```

## 📊 Sample Data

The setup includes sample sales data from [sibaramkumar/dataFiles](https://github.com/sibaramkumar/dataFiles) that can be loaded into HDFS.

### Downloading and Loading Sample Data

The sample data (`SalesData.zip`) contains sales-related datasets. Here's how to download and load it into HDFS:

```bash
# Download the SalesData.zip file
curl -L -o /tmp/SalesData.zip https://github.com/sibaramkumar/dataFiles/raw/main/SalesData.zip

# Extract the ZIP file
unzip -q /tmp/SalesData.zip -d /tmp/extracted

# Copy extracted files to HDFS
docker cp /tmp/extracted namenode:/tmp/extracted
docker exec namenode hadoop fs -mkdir -p /data/sales
docker exec namenode hadoop fs -put /tmp/extracted/* /data/sales/

# Verify files are in HDFS
docker exec namenode hadoop fs -ls /data/sales
```

### Available Datasets

Once loaded, the following datasets will be available in HDFS at `/data/sales/`:

- `customers` - Customer information (customer_id, name, address, etc.)
- `products` - Product catalog (product_id, name, price, category, etc.)
- `orders` - Order records (order_id, date, customer_id, status)
- `order_items` - Order line items (order_item_id, order_id, product_id, quantity, etc.)
- `categories` - Product categories (category_id, department_id, name)
- `departments` - Department information (department_id, name)

### Using the Sample Data

See `jupyter-work/access_hdfs_data.py` for examples on how to load and analyze this data in Spark:

```python
from access_hdfs_data import *

# All datasets are automatically loaded and ready to use
# Example: Join orders with customers
orders_with_customers = orders_df.join(
    customers_df, 
    orders_df.order_customer_id == customers_df.customer_id,
    "inner"
)
orders_with_customers.show(5)
```

## ⚙️ Configuration

### Spark Configuration

The `spark_helper.py` module configures Spark with:

- **Master**: `spark://spark-master:7077` (cluster mode)
- **HDFS**: `hdfs://namenode:8020` (default filesystem)
- **Python**: Ensures Python 3.10 consistency between driver and workers
- **Network**: Configured for Docker container communication

### Environment Variables

- `SPARK_MASTER`: Spark master URL (default: `spark://spark-master:7077`)
- `HDFS_NAMENODE`: HDFS NameNode address (default: `namenode:8020`)

## 🔧 Management Commands

```bash
# Stop all services
docker-compose -f docker-compose-spark35.yml down

# Restart a specific service
docker-compose -f docker-compose-spark35.yml restart jupyter-pyspark

# View logs for a service
docker-compose -f docker-compose-spark35.yml logs -f spark-master

# Scale Spark workers (if needed)
docker-compose -f docker-compose-spark35.yml up -d --scale spark-worker=2
```

## 📁 Project Structure

```
.
├── docker-compose-spark35.yml    # Main Docker Compose configuration
├── Dockerfile.jupyter-spark35    # Jupyter notebook image with PySpark
├── hadoop-spark35.env            # Hadoop configuration
├── README-SPARK35.md            # This file
└── jupyter-work/                 # Jupyter notebook workspace
    ├── spark_helper.py           # Spark session initialization helper
    ├── access_hdfs_data.py       # HDFS data access examples
    └── hdfs_filesystem.py        # HDFS filesystem utilities
```

## 🐛 Troubleshooting

### Workers not accepting resources

If you see warnings about resources not being accepted:
1. Restart your Jupyter kernel
2. Verify workers are registered: Check http://localhost:8080
3. Ensure `spark.driver.host` is set correctly in `spark_helper.py`

### Python version mismatch

Ensure Python versions match between driver and workers (both should be 3.10).

### HDFS connection issues

Verify HDFS is running:
```bash
docker exec namenode hadoop fs -ls /
```

## 📚 Key Features

- ✅ **Spark 3.5.7** with Adaptive Query Execution (AQE)
- ✅ **Cluster mode** execution (not local)
- ✅ **HDFS integration** for distributed storage
- ✅ **Jupyter notebooks** for interactive development
- ✅ **Sample data** pre-loaded for testing
- ✅ **Modern Docker images** from official sources

## 🔗 Useful Links

- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [HDFS Documentation](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)

## 📄 License

This setup is based on the [big-data-europe/docker-hadoop-spark-workbench](https://github.com/big-data-europe/docker-hadoop-spark-workbench) project, adapted for Spark 3.5.

