-- ============================================
-- Brazilian E-Commerce Analysis
-- SQL Customer Analysis
-- ============================================


-- 1. Total Unique Customers

SELECT
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;


-- 2. One-Time vs Repeat Customers

SELECT
    COUNT(*) FILTER (WHERE order_count = 1) AS one_time_customers,
    COUNT(*) FILTER (WHERE order_count > 1) AS repeat_customers
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) customer_orders;


-- 3. Repeat Customer Rate

SELECT
    ROUND(
        COUNT(*) FILTER (WHERE order_count > 1)::NUMERIC
        / COUNT(*) * 100,
        2
    ) AS repeat_customer_rate_pct
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) customer_orders;


-- 4. Customer Distribution by State

SELECT
    customer_state,
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers
GROUP BY customer_state
ORDER BY unique_customers DESC;


-- 5. Customer State Revenue and Customer Count

SELECT
    c.customer_state,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;