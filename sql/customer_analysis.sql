WITH completed_sales AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        c.customer_name,
        c.region,
        oi.revenue,
        oi.profit
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'Completed'
),
customer_rollup AS (
    SELECT
        customer_id,
        customer_name,
        region,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS avg_spend_per_order
    FROM completed_sales
    GROUP BY customer_id, customer_name, region
)
SELECT *
FROM customer_rollup
ORDER BY total_revenue DESC
LIMIT 10;

SELECT *
FROM customer_rollup
ORDER BY total_profit DESC
LIMIT 10;

SELECT
    CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-time Customer' END AS customer_type,
    COUNT(*) AS customers
FROM customer_rollup
GROUP BY CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-time Customer' END;

SELECT
    customer_id,
    customer_name,
    total_revenue,
    ROUND(total_revenue * 100.0 / NULLIF(SUM(total_revenue) OVER (), 0), 2) AS revenue_contribution_pct
FROM customer_rollup
ORDER BY total_revenue DESC
LIMIT 15;

WITH purchase_gaps AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS days_between_orders
    FROM (
        SELECT DISTINCT customer_id, order_id, order_date
        FROM completed_sales
    )
)
SELECT ROUND(AVG(days_between_orders), 2) AS average_days_between_orders
FROM purchase_gaps
WHERE days_between_orders IS NOT NULL;
