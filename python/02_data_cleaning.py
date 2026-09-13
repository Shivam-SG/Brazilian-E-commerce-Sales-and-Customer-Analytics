# ============================================
# Brazilian E-Commerce Analysis
# Python - Data Cleaning & Transformation
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


# 2. Convert order date columns to datetime

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# 3. Convert review date columns to datetime

review_date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in review_date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )


# 4. Check converted date columns

print("Orders Date Data Types")
print("----------------------")
print(orders[date_columns].dtypes)


# 5. Handle missing product categories

products["product_category_name"] = products[
    "product_category_name"
].fillna("Unclassified")


# 6. Merge English category names

products = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)


# 7. Handle categories without English translation

products["product_category_name_english"] = products[
    "product_category_name_english"
].fillna("Unclassified")


# 8. Check category mapping

print("\nProduct Category Mapping")
print("------------------------")

print(
    products[
        [
            "product_category_name",
            "product_category_name_english"
        ]
    ].head(10)
)


# 9. Check remaining missing values

print("\nMissing Values - Orders")
print("-----------------------")
print(orders.isnull().sum())


print("\nMissing Values - Products")
print("-------------------------")
print(products.isnull().sum())


# 10. Check duplicate IDs

print("\nDuplicate ID Checks")
print("-------------------")

print(
    "Duplicate Customer IDs:",
    customers["customer_id"].duplicated().sum()
)

print(
    "Duplicate Order IDs:",
    orders["order_id"].duplicated().sum()
)

print(
    "Duplicate Product IDs:",
    products["product_id"].duplicated().sum()
)

print(
    "Duplicate Seller IDs:",
    sellers["seller_id"].duplicated().sum()
)


# 11. Create order month

orders["order_month"] = orders[
    "order_purchase_timestamp"
].dt.to_period("M").astype(str)


# 12. Create delivery status

orders["delivery_status"] = "Delivery Date Missing"

orders.loc[
    orders["order_delivered_customer_date"].notna()
    & (
        orders["order_delivered_customer_date"]
        <= orders["order_estimated_delivery_date"]
    ),
    "delivery_status"
] = "On Time"

orders.loc[
    orders["order_delivered_customer_date"].notna()
    & (
        orders["order_delivered_customer_date"]
        > orders["order_estimated_delivery_date"]
    ),
    "delivery_status"
] = "Late"


# 13. Display delivery status distribution

print("\nDelivery Status Distribution")
print("----------------------------")
print(
    orders["delivery_status"]
    .value_counts()
)


# 14. Create delivery time in days

orders["delivery_time_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400


# 15. Display average delivery time

print("\nAverage Delivery Time")
print("---------------------")

print(
    round(
        orders["delivery_time_days"].mean(),
        2
    ),
    "days"
)