-- ============================================
-- Brazilian E-Commerce Analysis
-- SQL Review Analysis
-- ============================================


-- 1. Overall Review Score Distribution

SELECT
    review_score,
    COUNT(*) AS review_count,

    ROUND(
        COUNT(*)::NUMERIC
        / (SELECT COUNT(*) FROM order_reviews) * 100,
        2
    ) AS review_share_pct

FROM order_reviews

GROUP BY review_score

ORDER BY review_score;


-- 2. Average Review Score

SELECT
    ROUND(
        AVG(review_score),
        2
    ) AS average_review_score

FROM order_reviews;


-- 3. Delivery Performance vs Review Score

SELECT
    CASE
        WHEN o.order_delivered_customer_date IS NULL
            THEN 'Delivery Date Missing'

        WHEN o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Late'
    END AS delivery_status,

    COUNT(DISTINCT r.order_id) AS reviewed_orders,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score

FROM order_reviews r

JOIN orders o
    ON r.order_id = o.order_id

GROUP BY
    CASE
        WHEN o.order_delivered_customer_date IS NULL
            THEN 'Delivery Date Missing'

        WHEN o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Late'
    END

ORDER BY average_review_score DESC;


-- 4. 5-Star Review Share by Delivery Status

SELECT
    CASE
        WHEN o.order_delivered_customer_date IS NULL
            THEN 'Delivery Date Missing'

        WHEN o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Late'
    END AS delivery_status,

    COUNT(*) AS total_reviews,

    COUNT(*) FILTER (
        WHERE r.review_score = 5
    ) AS five_star_reviews,

    ROUND(
        COUNT(*) FILTER (
            WHERE r.review_score = 5
        )::NUMERIC
        / COUNT(*) * 100,
        2
    ) AS five_star_share_pct

FROM order_reviews r

JOIN orders o
    ON r.order_id = o.order_id

GROUP BY
    CASE
        WHEN o.order_delivered_customer_date IS NULL
            THEN 'Delivery Date Missing'

        WHEN o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Late'
    END

ORDER BY five_star_share_pct DESC;


-- 5. Low Review Score Share by Delivery Status
-- Low score = 1 or 2 stars

SELECT
    CASE
        WHEN o.order_delivered_customer_date IS NULL
            THEN 'Delivery Date Missing'

        WHEN o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Late'
    END AS delivery_status,

    COUNT(*) AS total_reviews,

    COUNT(*) FILTER (
        WHERE r.review_score IN (1, 2)
    ) AS low_score_reviews,

    ROUND(
        COUNT(*) FILTER (
            WHERE r.review_score IN (1, 2)
        )::NUMERIC
        / COUNT(*) * 100,
        2
    ) AS low_score_share_pct

FROM order_reviews r

JOIN orders o
    ON r.order_id = o.order_id

GROUP BY
    CASE
        WHEN o.order_delivered_customer_date IS NULL
            THEN 'Delivery Date Missing'

        WHEN o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Late'
    END

ORDER BY low_score_share_pct DESC;


-- 6. Average Review Score by Product Category

SELECT
    COALESCE(
        p.product_category_name,
        'Unclassified'
    ) AS product_category,

    COUNT(DISTINCT r.order_id) AS reviewed_orders,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score,

    ROUND(
        COUNT(*) FILTER (
            WHERE r.review_score IN (1, 2)
        )::NUMERIC
        / COUNT(*) * 100,
        2
    ) AS low_score_share_pct

FROM order_reviews r

JOIN order_items oi
    ON r.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY
    COALESCE(
        p.product_category_name,
        'Unclassified'
    )

HAVING COUNT(DISTINCT r.order_id) >= 100

ORDER BY average_review_score ASC;


-- 7. Lowest-Rated Categories
-- Minimum 100 reviewed orders to avoid small-sample results

SELECT
    COALESCE(
        p.product_category_name,
        'Unclassified'
    ) AS product_category,

    COUNT(DISTINCT r.order_id) AS reviewed_orders,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score

FROM order_reviews r

JOIN order_items oi
    ON r.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY
    COALESCE(
        p.product_category_name,
        'Unclassified'
    )

HAVING COUNT(DISTINCT r.order_id) >= 100

ORDER BY average_review_score ASC

LIMIT 10;