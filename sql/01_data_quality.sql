-- ============================================
-- Brazilian E-Commerce Analysis
-- SQL Data Quality Checks
-- ============================================

-- 1. Row counts
SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers
UNION ALL
SELECT 'orders', COUNT(*)
FROM orders
UNION ALL
SELECT 'order_items', COUNT(*)
FROM order_items
UNION ALL
SELECT 'products', COUNT(*)
FROM products
UNION ALL
SELECT 'sellers', COUNT(*)
FROM sellers
UNION ALL
SELECT 'category_translation', COUNT(*)
FROM category_translation;


-- 2. Orders without matching customers
SELECT COUNT(*) AS orders_without_customer
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- 3. Order items without matching orders
SELECT COUNT(*) AS order_items_without_order
FROM order_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 4. Order items without matching products
SELECT COUNT(*) AS order_items_without_product
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- 5. Order items without matching sellers
SELECT COUNT(*) AS order_items_without_seller
FROM order_items oi
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;


-- 6. Product category completeness
SELECT
    COUNT(*) AS total_products,
    COUNT(product_category_name) AS products_with_category,
    COUNT(*) - COUNT(product_category_name) AS missing_categories
FROM products;


-- 7. Product category translation coverage
SELECT
    COUNT(*) AS products_with_category,
    COUNT(ct.product_category_name) AS translated_category_matches,
    COUNT(*) - COUNT(ct.product_category_name) AS untranslated_category_matches
FROM products p
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE p.product_category_name IS NOT NULL;


-- 8. Order item critical-field completeness
SELECT
    COUNT(*) AS total_order_items,
    COUNT(order_id) AS order_ids_present,
    COUNT(product_id) AS product_ids_present,
    COUNT(seller_id) AS seller_ids_present,
    COUNT(price) AS prices_present,
    COUNT(freight_value) AS freight_values_present
FROM order_items;