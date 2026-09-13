# ============================================
# Brazilian E-Commerce Analysis
# Python - Delivery & Review Analysis
# ============================================

import pandas as pd


# ============================================
# 1. Load Datasets
# ============================================

orders = pd.read_csv(
    "./data/raw/olist_orders_dataset.csv"
)

reviews = pd.read_csv(
    "./data/raw/olist_order_reviews_dataset.csv"
)

order_items = pd.read_csv(
    "./data/raw/olist_order_items_dataset.csv"
)

products = pd.read_csv(
    "./data/raw/olist_products_dataset.csv"
)


# ============================================
# 2. Convert Order Dates
# ============================================

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# ============================================
# 3. Create Delivery Status
# ============================================

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


# ============================================
# 4. Delivery Performance Summary
# ============================================

delivery_counts = (
    orders["delivery_status"]
    .value_counts()
)

delivered_orders = (
    orders["order_delivered_customer_date"]
    .notna()
    .sum()
)

on_time_orders = (
    orders["delivery_status"]
    .eq("On Time")
    .sum()
)

late_orders = (
    orders["delivery_status"]
    .eq("Late")
    .sum()
)

missing_delivery_date = (
    orders["delivery_status"]
    .eq("Delivery Date Missing")
    .sum()
)

on_time_rate = (
    on_time_orders
    / delivered_orders
    * 100
)

late_rate = (
    late_orders
    / delivered_orders
    * 100
)


print("\n============================================")
print("DELIVERY PERFORMANCE")
print("============================================")

print(
    f"Total Orders: {len(orders):,}"
)

print(
    f"Delivered Orders: {delivered_orders:,}"
)

print(
    f"On-Time Orders: {on_time_orders:,}"
)

print(
    f"Late Orders: {late_orders:,}"
)

print(
    f"Missing Delivery Date: "
    f"{missing_delivery_date:,}"
)

print(
    f"On-Time Rate: {on_time_rate:.2f}%"
)

print(
    f"Late Rate: {late_rate:.2f}%"
)


# ============================================
# 5. Average Delivery Time
# ============================================

orders["delivery_time_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400

average_delivery_days = (
    orders["delivery_time_days"]
    .mean()
)


print(
    f"\nAverage Delivery Time: "
    f"{average_delivery_days:.2f} days"
)


# ============================================
# 6. Monthly Late Delivery Rate
# ============================================

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

monthly_delivery = (
    orders
    .groupby("order_month")
    .agg(
        delivered_orders=(
            "order_delivered_customer_date",
            "count"
        ),
        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        )
    )
    .reset_index()
)

monthly_delivery["late_rate_pct"] = (
    monthly_delivery["late_orders"]
    / monthly_delivery["delivered_orders"]
    * 100
)

monthly_delivery["late_rate_pct"] = (
    monthly_delivery["late_rate_pct"]
    .round(2)
)


print("\n============================================")
print("MONTHLY LATE DELIVERY RATE")
print("============================================")

print(
    monthly_delivery.to_string(index=False)
)


# ============================================
# 7. Highest Meaningful Late-Delivery Months
# ============================================

meaningful_months = (
    monthly_delivery[
        monthly_delivery["delivered_orders"] >= 1000
    ]
    .sort_values(
        "late_rate_pct",
        ascending=False
    )
)

print("\n============================================")
print("HIGHEST MEANINGFUL LATE-DELIVERY MONTHS")
print("============================================")

print(
    meaningful_months.head(5).to_string(index=False)
)


# ============================================
# 8. Average Delay for Late Orders
# ============================================

late_orders_data = orders[
    orders["delivery_status"] == "Late"
].copy()

late_orders_data["delay_days"] = (
    late_orders_data[
        "order_delivered_customer_date"
    ]
    - late_orders_data[
        "order_estimated_delivery_date"
    ]
).dt.total_seconds() / 86400

average_delay_days = (
    late_orders_data["delay_days"].mean()
)


print(
    f"\nAverage Delay for Late Orders: "
    f"{average_delay_days:.2f} days"
)


# ============================================
# 9. Review Data
# ============================================

reviews["review_creation_date"] = pd.to_datetime(
    reviews["review_creation_date"],
    errors="coerce"
)

reviews["review_answer_timestamp"] = pd.to_datetime(
    reviews["review_answer_timestamp"],
    errors="coerce"
)


# ============================================
# 10. Overall Review Analysis
# ============================================

average_review_score = (
    reviews["review_score"].mean()
)

review_distribution = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

five_star_share = (
    reviews["review_score"]
    .eq(5)
    .mean()
    * 100
)


print("\n============================================")
print("CUSTOMER REVIEW ANALYSIS")
print("============================================")

print(
    f"Total Reviews: {len(reviews):,}"
)

print(
    f"Average Review Score: "
    f"{average_review_score:.2f}"
)

print(
    f"5-Star Review Share: "
    f"{five_star_share:.2f}%"
)

print("\nReview Distribution:")

print(
    review_distribution
)


# ============================================
# 11. Delivery Status vs Review Score
# ============================================

review_delivery = (
    reviews[
        [
            "order_id",
            "review_score"
        ]
    ]
    .merge(
        orders[
            [
                "order_id",
                "delivery_status"
            ]
        ],
        on="order_id",
        how="inner"
    )
)

delivery_review_summary = (
    review_delivery
    .groupby("delivery_status")
    .agg(
        reviewed_orders=(
            "order_id",
            "nunique"
        ),
        average_review_score=(
            "review_score",
            "mean"
        ),
        five_star_share=(
            "review_score",
            lambda x: (x == 5).mean() * 100
        )
    )
    .reset_index()
)

delivery_review_summary[
    "average_review_score"
] = (
    delivery_review_summary[
        "average_review_score"
    ].round(2)
)

delivery_review_summary[
    "five_star_share"
] = (
    delivery_review_summary[
        "five_star_share"
    ].round(2)
)


print("\n============================================")
print("DELIVERY STATUS VS REVIEW SCORE")
print("============================================")

print(
    delivery_review_summary.to_string(index=False)
)


# ============================================
# 12. Low Review Score Share by Delivery Status
# ============================================

review_delivery["low_score"] = (
    review_delivery["review_score"]
    .isin([1, 2])
)

low_score_summary = (
    review_delivery
    .groupby("delivery_status")
    .agg(
        total_reviews=(
            "review_score",
            "count"
        ),
        low_score_reviews=(
            "low_score",
            "sum"
        )
    )
    .reset_index()
)

low_score_summary["low_score_share_pct"] = (
    low_score_summary["low_score_reviews"]
    / low_score_summary["total_reviews"]
    * 100
)

low_score_summary[
    "low_score_share_pct"
] = (
    low_score_summary[
        "low_score_share_pct"
    ].round(2)
)


print("\n============================================")
print("LOW REVIEW SCORE SHARE")
print("============================================")

print(
    low_score_summary.to_string(index=False)
)


# ============================================
# 13. Review Score by Product Category
# ============================================

category_reviews = (
    reviews[
        [
            "order_id",
            "review_score"
        ]
    ]
    .merge(
        order_items[
            [
                "order_id",
                "product_id"
            ]
        ],
        on="order_id",
        how="inner"
    )
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

category_reviews[
    "product_category_name"
] = (
    category_reviews[
        "product_category_name"
    ]
    .fillna("Unclassified")
)


category_review_summary = (
    category_reviews
    .groupby("product_category_name")
    .agg(
        reviewed_orders=(
            "order_id",
            "nunique"
        ),
        average_review_score=(
            "review_score",
            "mean"
        ),
        low_score_share=(
            "review_score",
            lambda x: x.isin([1, 2]).mean() * 100
        )
    )
    .reset_index()
)

category_review_summary = (
    category_review_summary[
        category_review_summary["reviewed_orders"] >= 100
    ]
    .sort_values(
        "average_review_score"
    )
)

category_review_summary[
    "average_review_score"
] = (
    category_review_summary[
        "average_review_score"
    ].round(2)
)

category_review_summary[
    "low_score_share"
] = (
    category_review_summary[
        "low_score_share"
    ].round(2)
)


print("\n============================================")
print("LOWEST-RATED PRODUCT CATEGORIES")
print("============================================")

print(
    category_review_summary
    .head(10)
    .to_string(index=False)
)