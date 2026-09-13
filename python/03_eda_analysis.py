# ============================================
# Brazilian E-Commerce Analysis
# Python - EDA & Core KPI Analysis
# ============================================

import pandas as pd


# 1. Load datasets

customers = pd.read_csv("./data/raw/olist_customers_dataset.csv")
orders = pd.read_csv("./data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("./data/raw/olist_order_items_dataset.csv")
products = pd.read_csv("./data/raw/olist_products_dataset.csv")
sellers = pd.read_csv("./data/raw/olist_sellers_dataset.csv")


# 2. Convert order dates

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


# ============================================
# 3. CORE KPIs
# ============================================

total_revenue = order_items["price"].sum()

total_orders = orders["order_id"].nunique()

average_order_value = total_revenue / total_orders

average_items_per_order = round(
    len(order_items) / total_orders,
    2
)

average_delivery_days = (
    orders["delivery_time_days"].mean()
    if "delivery_time_days" in orders.columns
    else (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds().div(86400).mean()
)


print("\n============================================")
print("CORE BUSINESS KPIs")
print("============================================")

print(
    f"Total Revenue: R$ {total_revenue:,.2f}"
)

print(
    f"Total Orders: {total_orders:,}"
)

print(
    f"Average Order Value: R$ {average_order_value:,.2f}"
)

print(
    f"Average Items per Order: "
    f"{average_items_per_order:.2f}"
)

print(
    f"Average Delivery Time: "
    f"{average_delivery_days:.2f} days"
)


# ============================================
# 4. MONTHLY REVENUE ANALYSIS
# ============================================

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

monthly_revenue = (
    orders[
        [
            "order_id",
            "order_month"
        ]
    ]
    .merge(
        order_items[
            [
                "order_id",
                "price"
            ]
        ],
        on="order_id",
        how="inner"
    )
    .groupby("order_month")
    .agg(
        monthly_revenue=("price", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

monthly_revenue["monthly_revenue"] = (
    monthly_revenue["monthly_revenue"].round(2)
)

monthly_revenue["mom_growth_pct"] = (
    monthly_revenue["monthly_revenue"]
    .pct_change()
    .mul(100)
    .round(2)
)


print("\n============================================")
print("MONTHLY REVENUE")
print("============================================")

print(
    monthly_revenue.to_string(index=False)
)


# ============================================
# 5. TOP 10 PRODUCT CATEGORIES
# ============================================

category_revenue = (
    order_items
    .merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )
    .assign(
        product_category_name=lambda x:
        x["product_category_name"].fillna("Unclassified")
    )
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

top_10_categories = (
    category_revenue
    .head(10)
    .round(2)
)

top_10_category_revenue = (
    top_10_categories.sum()
)

top_10_category_share = (
    top_10_category_revenue
    / total_revenue
    * 100
)


print("\n============================================")
print("TOP 10 PRODUCT CATEGORIES")
print("============================================")

print(top_10_categories)

print(
    f"\nTop 10 Category Revenue: "
    f"R$ {top_10_category_revenue:,.2f}"
)

print(
    f"Top 10 Category Revenue Share: "
    f"{top_10_category_share:.2f}%"
)


# ============================================
# 6. TOP 10 SELLERS
# ============================================

seller_revenue = (
    order_items
    .groupby("seller_id")
    .agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique")
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
)

top_10_sellers = seller_revenue.head(10).copy()

top_10_seller_revenue = (
    top_10_sellers["total_revenue"].sum()
)

top_10_seller_share = (
    top_10_seller_revenue
    / total_revenue
    * 100
)


print("\n============================================")
print("TOP 10 SELLERS")
print("============================================")

print(
    top_10_sellers.round(2)
)

print(
    f"\nTop 10 Seller Revenue: "
    f"R$ {top_10_seller_revenue:,.2f}"
)

print(
    f"Top 10 Seller Revenue Share: "
    f"{top_10_seller_share:.2f}%"
)


# ============================================
# 7. CUSTOMER ANALYSIS
# ============================================

customer_orders = (
    customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_state"
        ]
    ]
    .merge(
        orders[
            [
                "order_id",
                "customer_id"
            ]
        ],
        on="customer_id",
        how="inner"
    )
    .groupby("customer_unique_id")
    .agg(
        order_count=("order_id", "nunique")
    )
)

unique_customers = len(customer_orders)

one_time_customers = (
    customer_orders["order_count"]
    .eq(1)
    .sum()
)

repeat_customers = (
    customer_orders["order_count"]
    .gt(1)
    .sum()
)

repeat_customer_rate = (
    repeat_customers
    / unique_customers
    * 100
)


print("\n============================================")
print("CUSTOMER ANALYSIS")
print("============================================")

print(
    f"Unique Customers: {unique_customers:,}"
)

print(
    f"One-Time Customers: {one_time_customers:,}"
)

print(
    f"Repeat Customers: {repeat_customers:,}"
)

print(
    f"Repeat Customer Rate: "
    f"{repeat_customer_rate:.2f}%"
)


# ============================================
# 8. CUSTOMER STATE DISTRIBUTION
# ============================================

customer_state_counts = (
    customers
    .groupby("customer_state")["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n============================================")
print("CUSTOMERS BY STATE")
print("============================================")

print(
    customer_state_counts.head(10)
)


# ============================================
# 9. SELLER STATE REVENUE
# ============================================

seller_state_revenue = (
    order_items
    .merge(
        sellers[
            [
                "seller_id",
                "seller_state"
            ]
        ],
        on="seller_id",
        how="left"
    )
    .groupby("seller_state")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\n============================================")
print("REVENUE BY SELLER STATE")
print("============================================")

print(
    seller_state_revenue.head(10).round(2)
)