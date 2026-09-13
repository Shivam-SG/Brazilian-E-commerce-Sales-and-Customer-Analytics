-- ============================================
-- Brazilian E-Commerce Analysis
-- SQL KPI Analysis
-- ============================================


-- 1. Total Revenue
-- Revenue is defined as the sum of item prices.
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;


-- 2. Total Orders
SELECT
    COUNT(*) AS total_orders
FROM orders;


-- 3. Average Order Value (AOV)
-- Project definition:
-- Total Revenue / Total Orders
SELECT
    ROUND(
        (SELECT SUM(price) FROM order_items)
        /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS average_order_value;


-- 4. Average Items per Order
SELECT
    ROUND(
        COUNT(*)::NUMERIC
        / COUNT(DISTINCT order_id),
        2
    ) AS average_items_per_order
FROM order_items;


-- 5. Average Delivery Time in Days
SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date
                    - order_purchase_timestamp
                )
            ) / 86400
        ),
        2
    ) AS avg_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;


-- 6. Delivery Date Availability
SELECT
    COUNT(*) AS total_orders,
    COUNT(order_delivered_customer_date) AS delivered_orders,
    COUNT(*) - COUNT(order_delivered_customer_date)
        AS missing_delivery_date
FROM orders;


-- 7. On-Time vs Late Delivery Rate
SELECT
    ROUND(
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_delivered_customer_date
                  <= order_estimated_delivery_date
        )::NUMERIC
        /
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
        ) * 100,
        2
    ) AS on_time_rate_pct,

    ROUND(
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_delivered_customer_date
                  > order_estimated_delivery_date
        )::NUMERIC
        /
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
        ) * 100,
        2
    ) AS late_rate_pct
FROM orders;