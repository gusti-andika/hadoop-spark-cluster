"""
Example: Access Sales Data from HDFS using Spark
The SalesData.zip has been extracted to /data/sales/ with the following directories:
- categories
- customers
- departments
- order_items
- orders
- products
"""
from spark_helper import init_spark

# Initialize Spark
spark = init_spark("Sales Data Analysis")

# Base HDFS path
base_path = "hdfs://namenode:8020/data/sales"

# Read each dataset
print("Loading sales data from HDFS...")

# Read customers (CSV without headers)
# Columns: customer_id, first_name, last_name, email, password, street, city, state, zipcode
customers_df = spark.read.csv(f"{base_path}/customers/*", header=False, inferSchema=True)
customers_df = customers_df.toDF("customer_id", "first_name", "last_name", "email", "password", 
                                  "street", "city", "state", "zipcode")
print(f"Customers: {customers_df.count()} rows")
customers_df.show(5)

# Read products (CSV without headers)
# Columns: product_id, product_category_id, product_name, product_description, product_price, product_image
products_df = spark.read.csv(f"{base_path}/products/*", header=False, inferSchema=True)
products_df = products_df.toDF("product_id", "product_category_id", "product_name", 
                               "product_description", "product_price", "product_image")
print(f"\nProducts: {products_df.count()} rows")
products_df.show(5)

# Read orders (CSV without headers)
# Columns: order_id, order_date, order_customer_id, order_status
orders_df = spark.read.csv(f"{base_path}/orders/*", header=False, inferSchema=True)
orders_df = orders_df.toDF("order_id", "order_date", "order_customer_id", "order_status")
print(f"\nOrders: {orders_df.count()} rows")
orders_df.show(5)

# Read order_items (CSV without headers)
# Columns: order_item_id, order_item_order_id, order_item_product_id, order_item_quantity, order_item_subtotal, order_item_product_price
order_items_df = spark.read.csv(f"{base_path}/order_items/*", header=False, inferSchema=True)
order_items_df = order_items_df.toDF("order_item_id", "order_item_order_id", "order_item_product_id",
                                      "order_item_quantity", "order_item_subtotal", "order_item_product_price")
print(f"\nOrder Items: {order_items_df.count()} rows")
order_items_df.show(5)

# Read categories (CSV without headers)
# Columns: category_id, category_department_id, category_name
categories_df = spark.read.csv(f"{base_path}/categories/*", header=False, inferSchema=True)
categories_df = categories_df.toDF("category_id", "category_department_id", "category_name")
print(f"\nCategories: {categories_df.count()} rows")
categories_df.show(5)

# Read departments (CSV without headers)
# Columns: department_id, department_name
departments_df = spark.read.csv(f"{base_path}/departments/*", header=False, inferSchema=True)
departments_df = departments_df.toDF("department_id", "department_name")
print(f"\nDepartments: {departments_df.count()} rows")
departments_df.show(5)

print("\nAll datasets loaded successfully!")

