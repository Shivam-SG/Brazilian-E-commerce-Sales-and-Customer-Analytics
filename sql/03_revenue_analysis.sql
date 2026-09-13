-- ============================================
-- Brazilian E-Commerce Analysis
-- SQL Revenue Analysis
-- ============================================


-- 1. Monthly Revenue Trend

SELECT
    TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS order_month,
    ROUND(SUM(oi.price), 2) AS monthly_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM')
ORDER BY order_month;


-- 2. Top 10 Product Categories by Revenue

SELECT
    p.product_category_name AS product_category,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. Top 10 Product Category Revenue Share

WITH category_sales AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS total_revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
),
ranked_categories AS (
    SELECT
        product_category_name,
        total_revenue,
        RANK() OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM category_sales
)
SELECT
    ROUND(SUM(total_revenue), 2) AS top_10_revenue,
    ROUND(
        SUM(total_revenue)
        / (SELECT SUM(price) FROM order_items)
        * 100,
        2
    ) AS top_10_revenue_share_pct
FROM ranked_categories
WHERE revenue_rank <= 10;


-- 4. Top 10 Sellers by Revenue

SELECT
    seller_id,
    ROUND(SUM(price), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM order_items
GROUP BY seller_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Top 10 Seller Revenue Share

WITH seller_sales AS (
    SELECT
        seller_id,
        SUM(price) AS total_revenue
    FROM order_items
    GROUP BY seller_id
),
ranked_sellers AS (
    SELECT
        seller_id,
        total_revenue,
        RANK() OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM seller_sales
)
SELECT
    ROUND(SUM(total_revenue), 2) AS top_10_seller_revenue,
    ROUND(
        SUM(total_revenue)
        / (SELECT SUM(price) FROM order_items)
        * 100,
        2
    ) AS top_10_seller_revenue_share_pct
FROM ranked_sellers
WHERE revenue_rank <= 10;


-- 6. Revenue by Customer State

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


-- 7. Customer State Revenue Share

SELECT
    c.customer_state,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(
        SUM(oi.price)
        / (SELECT SUM(price) FROM order_items)
        * 100,
        2
    ) AS revenue_share_pct
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;


-- 8. Revenue by Seller State

SELECT
    s.seller_state,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    COUNT(DISTINCT oi.seller_id) AS total_sellers,
    COUNT(DISTINCT oi.order_id) AS total_orders
FROM order_items oi
JOIN sellers s
    ON oi.seller_id = s.seller_id
GROUP BY s.seller_state
ORDER BY total_revenue DESC;


-- 9. Seller State Revenue Share

SELECT
    s.seller_state,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(
        SUM(oi.price)
        / (SELECT SUM(price) FROM order_items)
        * 100,
        2
    ) AS revenue_share_pct
FROM order_items oi
JOIN sellers s
    ON oi.seller_id = s.seller_id
GROUP BY s.seller_state
ORDER BY total_revenue DESC;