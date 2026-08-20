WITH completed_sales AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        p.category,
        oi.discount,
        oi.revenue,
        oi.profit
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
),
discount_bands AS (
    SELECT
        CASE
            WHEN discount < 0.04 THEN 'Low Discount'
            WHEN discount < 0.08 THEN 'Medium Discount'
            ELSE 'High Discount'
        END AS discount_band,
        revenue,
        profit
    FROM completed_sales
),
customer_activity AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS orders,
        SUM(revenue) AS revenue
    FROM completed_sales
    GROUP BY customer_id
)
SELECT
    discount_band,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / NULLIF(SUM(revenue), 0)) * 100, 2) AS profit_margin_pct
FROM discount_bands
GROUP BY discount_band
ORDER BY revenue DESC;

SELECT
    CASE
        WHEN DATE '2025-01-01' - last_order_date <= 30 THEN 'Active'
        WHEN DATE '2025-01-01' - last_order_date <= 90 THEN 'Cooling Off'
        ELSE 'At Risk'
    END AS activity_bucket,
    COUNT(*) AS customers,
    ROUND(SUM(revenue), 2) AS revenue
FROM customer_activity
GROUP BY activity_bucket
ORDER BY revenue DESC;

SELECT
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    DENSE_RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM completed_sales
GROUP BY category
ORDER BY revenue_rank;
