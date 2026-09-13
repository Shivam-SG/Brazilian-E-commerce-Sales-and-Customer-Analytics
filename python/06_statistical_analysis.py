# ============================================
# Brazilian E-Commerce Analysis
# Python - Statistical Analysis
# ============================================

import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr


# ============================================
# 1. Load Datasets
# ============================================

orders = pd.read_csv(
    "./data/raw/olist_orders_dataset.csv"
)

reviews = pd.read_csv(
    "./data/raw/olist_order_reviews_dataset.csv"
)


# ============================================
# 2. Convert Dates
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
# 4. Merge Orders with Reviews
# ============================================

review_delivery = reviews[
    [
        "order_id",
        "review_score"
    ]
].merge(
    orders[
        [
            "order_id",
            "delivery_status",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ],
    on="order_id",
    how="inner"
)


# ============================================
# 5. Descriptive Statistics
# ============================================

print("\n============================================")
print("REVIEW SCORE DESCRIPTIVE STATISTICS")
print("============================================")

print(
    review_delivery["review_score"].describe()
)


# ============================================
# 6. Average Review Score by Delivery Status
# ============================================

status_summary = (
    review_delivery
    .groupby("delivery_status")["review_score"]
    .agg(
        count="count",
        mean="mean",
        median="median",
        std="std"
    )
    .round(2)
)

print("\n============================================")
print("REVIEW SCORE BY DELIVERY STATUS")
print("============================================")

print(status_summary)


# ============================================
# 7. Mann-Whitney U Test
# ============================================
#
# We compare review scores for:
# On-Time orders vs Late orders.
#
# Review scores are ordinal (1-5), so a
# non-parametric test is appropriate.
#
# H0: Review score distributions are the same.
# H1: Review score distributions are different.
# ============================================

on_time_scores = review_delivery.loc[
    review_delivery["delivery_status"] == "On Time",
    "review_score"
].dropna()

late_scores = review_delivery.loc[
    review_delivery["delivery_status"] == "Late",
    "review_score"
].dropna()


u_statistic, p_value = mannwhitneyu(
    on_time_scores,
    late_scores,
    alternative="two-sided"
)


print("\n============================================")
print("MANN-WHITNEY U TEST")
print("============================================")

print(
    f"U Statistic: {u_statistic:,.2f}"
)

print(
    f"P-Value: {p_value:.10f}"
)


# ============================================
# 8. Statistical Interpretation
# ============================================

alpha = 0.05

print("\nStatistical Interpretation")
print("--------------------------")

if p_value < alpha:
    print(
        "Result: Statistically significant difference "
        "between On-Time and Late review scores."
    )
    print(
        "Conclusion: Reject the null hypothesis "
        "at the 5% significance level."
    )
else:
    print(
        "Result: No statistically significant difference "
        "was detected."
    )
    print(
        "Conclusion: Fail to reject the null hypothesis "
        "at the 5% significance level."
    )


# ============================================
# 9. Delivery Delay vs Review Score
# ============================================

late_review_data = review_delivery[
    review_delivery["delivery_status"] == "Late"
].copy()

late_review_data["delay_days"] = (
    late_review_data[
        "order_delivered_customer_date"
    ]
    - late_review_data[
        "order_estimated_delivery_date"
    ]
).dt.total_seconds() / 86400


late_review_data = late_review_data.dropna(
    subset=[
        "delay_days",
        "review_score"
    ]
)


# ============================================
# 10. Spearman Correlation
# ============================================
#
# Tests whether greater delivery delay is
# associated with higher/lower review scores.
#
# H0: No monotonic relationship.
# H1: A monotonic relationship exists.
# ============================================

spearman_rho, spearman_p = spearmanr(
    late_review_data["delay_days"],
    late_review_data["review_score"]
)


print("\n============================================")
print("DELIVERY DELAY VS REVIEW SCORE")
print("============================================")

print(
    f"Spearman Correlation (rho): "
    f"{spearman_rho:.4f}"
)

print(
    f"P-Value: "
    f"{spearman_p:.10f}"
)


# ============================================
# 11. Correlation Interpretation
# ============================================

print("\nCorrelation Interpretation")
print("---------------------------")

if spearman_p < alpha:
    if spearman_rho < 0:
        print(
            "There is a statistically significant "
            "negative association between delivery "
            "delay and review score."
        )
    else:
        print(
            "There is a statistically significant "
            "positive association between delivery "
            "delay and review score."
        )
else:
    print(
        "No statistically significant monotonic "
        "association was detected."
    )


# ============================================
# 12. Important Limitation
# ============================================

print("\nImportant Limitation")
print("--------------------")

print(
    "Statistical association does not establish "
    "causation. Other factors may influence "
    "customer review scores."
)