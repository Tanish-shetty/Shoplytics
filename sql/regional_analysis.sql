WITH completed_sales AS (
    SELECT
        o.order_id,
        c.country,
        c.region,
        c.state,
        oi.revenue,
        oi.profit
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'Completed'
)
SELECT
    state,
    region,
    country,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / NULLIF(SUM(revenue), 0)) * 100, 2) AS profit_margin_pct
FROM completed_sales
GROUP BY state, region, country
ORDER BY revenue DESC;

SELECT
    region,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM completed_sales
GROUP BY region
ORDER BY revenue DESC;
