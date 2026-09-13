-- ============================================
-- Brazilian E-Commerce Analysis
-- SQL Delivery Analysis
-- ============================================


-- 1. Delivery Status Overview

SELECT
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NOT NULL
    ) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NULL
    ) AS missing_delivery_date

FROM orders;


-- 2. On-Time vs Late Delivery Count

SELECT
    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NOT NULL
          AND order_delivered_customer_date
              <= order_estimated_delivery_date
    ) AS on_time_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NOT NULL
          AND order_delivered_customer_date
              > order_estimated_delivery_date
    ) AS late_orders

FROM orders;


-- 3. On-Time vs Late Delivery Rate

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


-- 4. Average Delivery Time

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
    ) AS average_delivery_days

FROM orders

WHERE order_delivered_customer_date IS NOT NULL;


-- 5. Monthly Delivery Performance

SELECT
    TO_CHAR(
        order_purchase_timestamp,
        'YYYY-MM'
    ) AS order_month,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NOT NULL
    ) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NOT NULL
          AND order_delivered_customer_date
              <= order_estimated_delivery_date
    ) AS on_time_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date IS NOT NULL
          AND order_delivered_customer_date
              > order_estimated_delivery_date
    ) AS late_orders,

    ROUND(
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_delivered_customer_date
                  > order_estimated_delivery_date
        )::NUMERIC
        /
        NULLIF(
            COUNT(*) FILTER (
                WHERE order_delivered_customer_date IS NOT NULL
            ),
            0
        ) * 100,
        2
    ) AS late_rate_pct

FROM orders

GROUP BY
    TO_CHAR(
        order_purchase_timestamp,
        'YYYY-MM'
    )

ORDER BY order_month;


-- 6. Months with Highest Late Delivery Rate
-- Only months with at least 1,000 delivered orders
-- are included to avoid misleading small-sample results.

WITH monthly_delivery AS (
    SELECT
        TO_CHAR(
            order_purchase_timestamp,
            'YYYY-MM'
        ) AS order_month,

        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
        ) AS delivered_orders,

        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_delivered_customer_date
                  > order_estimated_delivery_date
        ) AS late_orders

    FROM orders

    GROUP BY
        TO_CHAR(
            order_purchase_timestamp,
            'YYYY-MM'
        )
)

SELECT
    order_month,
    delivered_orders,
    late_orders,

    ROUND(
        late_orders::NUMERIC
        / delivered_orders * 100,
        2
    ) AS late_rate_pct

FROM monthly_delivery

WHERE delivered_orders >= 1000

ORDER BY late_rate_pct DESC;


-- 7. Average Delivery Delay in Days
-- Positive value means the order arrived after
-- the estimated delivery date.

SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date
                    - order_estimated_delivery_date
                )
            ) / 86400
        ),
        2
    ) AS average_delivery_delay_days

FROM orders

WHERE order_delivered_customer_date IS NOT NULL
  AND order_delivered_customer_date
      > order_estimated_delivery_date;


-- 8. Delivery Performance by Customer State

SELECT
    c.customer_state,

    COUNT(*) FILTER (
        WHERE o.order_delivered_customer_date IS NOT NULL
    ) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE o.order_delivered_customer_date IS NOT NULL
          AND o.order_delivered_customer_date
              <= o.order_estimated_delivery_date
    ) AS on_time_orders,

    COUNT(*) FILTER (
        WHERE o.order_delivered_customer_date IS NOT NULL
          AND o.order_delivered_customer_date
              > o.order_estimated_delivery_date
    ) AS late_orders,

    ROUND(
        COUNT(*) FILTER (
            WHERE o.order_delivered_customer_date IS NOT NULL
              AND o.order_delivered_customer_date
                  > o.order_estimated_delivery_date
        )::NUMERIC
        /
        NULLIF(
            COUNT(*) FILTER (
                WHERE o.order_delivered_customer_date IS NOT NULL
            ),
            0
        ) * 100,
        2
    ) AS late_rate_pct

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

GROUP BY c.customer_state

ORDER BY late_rate_pct DESC;