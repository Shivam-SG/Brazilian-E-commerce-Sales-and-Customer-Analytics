# ============================================
# Brazilian E-Commerce Analysis
# Python - Data Loading & Initial Inspection
# ============================================

import pandas as pd


# 1. Load datasets

customers = pd.read_csv("./data/raw/olist_customers_dataset.csv")
orders = pd.read_csv("./data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("./data/raw/olist_order_items_dataset.csv")
products = pd.read_csv("./data/raw/olist_products_dataset.csv")
sellers = pd.read_csv("./data/raw/olist_sellers_dataset.csv")
reviews = pd.read_csv("./data/raw/olist_order_reviews_dataset.csv")
category_translation = pd.read_csv(
    "./data/raw/product_category_name_translation.csv"
)


# 2. Display dataset shapes

print("Dataset Shapes")
print("----------------")

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Reviews:", reviews.shape)
print("Category Translation:", category_translation.shape)


# 3. Display column names

print("\nCustomers Columns:")
print(customers.columns.tolist())

print("\nOrders Columns:")
print(orders.columns.tolist())

print("\nOrder Items Columns:")
print(order_items.columns.tolist())

print("\nProducts Columns:")
print(products.columns.tolist())

print("\nSellers Columns:")
print(sellers.columns.tolist())

print("\nReviews Columns:")
print(reviews.columns.tolist())

print("\nCategory Translation Columns:")
print(category_translation.columns.tolist())


# 4. Preview important datasets

print("\nCustomers Preview:")
print(customers.head())

print("\nOrders Preview:")
print(orders.head())

print("\nOrder Items Preview:")
print(order_items.head())


# 5. Missing value overview

print("\nMissing Values - Customers")
print(customers.isnull().sum())

print("\nMissing Values - Orders")
print(orders.isnull().sum())

print("\nMissing Values - Products")
print(products.isnull().sum())


# 6. Basic data types

print("\nOrders Data Types")
print(orders.dtypes)