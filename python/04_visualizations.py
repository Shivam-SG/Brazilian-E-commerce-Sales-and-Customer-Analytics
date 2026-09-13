# ============================================
# Brazilian E-Commerce Analysis
# Python - Data Visualizations
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================
# 1. Project Paths
# ============================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data/raw"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

SCREENSHOTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================
# 2. Load Datasets
# ============================================

orders = pd.read_csv(
    DATA_DIR / "olist_orders_dataset.csv"
)

order_items = pd.read_csv(
    DATA_DIR / "olist_order_items_dataset.csv"
)

products = pd.read_csv(
    DATA_DIR / "olist_products_dataset.csv"
)

sellers = pd.read_csv(
    DATA_DIR / "olist_sellers_dataset.csv"
)


# ============================================
# 3. Convert Order Date
# ============================================

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================
# 4. Monthly Revenue
# ============================================

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
    .groupby("order_month")["price"]
    .sum()
    .reset_index()
)

monthly_revenue["price"] = (
    monthly_revenue["price"].round(2)
)


# ============================================
# Chart 1 - Monthly Revenue Trend
# ============================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["order_month"],
    monthly_revenue["price"],
    marker="o"
)

plt.title(
    "Monthly Revenue Trend"
)

plt.xlabel(
    "Order Month"
)

plt.ylabel(
    "Revenue (R$)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "python_monthly_revenue.png",
    dpi=150
)

plt.close()


# ============================================
# 5. Top 10 Product Categories
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
)

category_revenue["product_category_name"] = (
    category_revenue["product_category_name"]
    .fillna("Unclassified")
)

category_revenue = (
    category_revenue
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)


# ============================================
# Chart 2 - Top 10 Product Categories
# ============================================

plt.figure(figsize=(10, 6))

plt.barh(
    category_revenue.index,
    category_revenue.values
)

plt.title(
    "Top 10 Product Categories by Revenue"
)

plt.xlabel(
    "Revenue (R$)"
)

plt.ylabel(
    "Product Category"
)

plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "python_top_10_categories.png",
    dpi=150
)

plt.close()


# ============================================
# 6. Revenue by Seller State
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


# ============================================
# Chart 3 - Revenue by Seller State
# ============================================

plt.figure(figsize=(10, 6))

plt.bar(
    seller_state_revenue.index,
    seller_state_revenue.values
)

plt.title(
    "Revenue by Seller State"
)

plt.xlabel(
    "Seller State"
)

plt.ylabel(
    "Revenue (R$)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "python_revenue_by_seller_state.png",
    dpi=150
)

plt.close()


# ============================================
# 7. Confirmation
# ============================================

print("\n============================================")
print("VISUALIZATIONS CREATED")
print("============================================")

print(
    "1. python_monthly_revenue.png"
)

print(
    "2. python_top_10_categories.png"
)

print(
    "3. python_revenue_by_seller_state.png"
)

print(
    f"\nSaved to: {SCREENSHOTS_DIR}"
)