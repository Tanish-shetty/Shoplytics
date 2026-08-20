WITH completed_lines AS (
    SELECT
        o.order_id,
        o.customer_id,
        oi.quantity,
        oi.revenue,
        oi.profit
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
),
customer_orders AS (
    SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
    FROM completed_lines
    GROUP BY customer_id
)
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT customer_id), 0), 2) AS average_revenue_per_customer,
    ROUND((SUM(profit) / NULLIF(SUM(revenue), 0)) * 100, 2) AS profit_margin,
    ROUND(
        (
            SELECT COUNT(*)
            FROM customer_orders
            WHERE order_count > 1
        ) * 100.0 / NULLIF(COUNT(DISTINCT customer_id), 0),
        2
    ) AS repeat_customer_rate
FROM completed_lines;
