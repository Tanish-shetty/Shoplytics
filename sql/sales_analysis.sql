WITH completed_sales AS (
    SELECT
        o.order_id,
        o.order_month,
        o.payment_method,
        c.region,
        p.category,
        p.sub_category,
        oi.revenue,
        oi.profit
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
),
monthly AS (
    SELECT
        order_month,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(SUM(revenue), 2) AS revenue,
        ROUND(SUM(profit), 2) AS profit
    FROM completed_sales
    GROUP BY order_month
)
SELECT
    order_month,
    order_count,
    revenue,
    profit,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY order_month))
        * 100.0
        / NULLIF(LAG(revenue) OVER (ORDER BY order_month), 0),
        2
    ) AS mom_revenue_growth_pct
FROM monthly
ORDER BY order_month;

SELECT order_month, revenue
FROM (
    SELECT order_month, ROUND(SUM(revenue), 2) AS revenue
    FROM completed_sales
    GROUP BY order_month
) monthly
ORDER BY revenue DESC
LIMIT 1;

SELECT order_month, revenue
FROM (
    SELECT order_month, ROUND(SUM(revenue), 2) AS revenue
    FROM completed_sales
    GROUP BY order_month
) monthly
ORDER BY revenue ASC
LIMIT 1;

SELECT category, ROUND(SUM(revenue), 2) AS revenue
FROM completed_sales
GROUP BY category
ORDER BY revenue DESC;

SELECT sub_category, ROUND(SUM(revenue), 2) AS revenue
FROM completed_sales
GROUP BY sub_category
ORDER BY revenue DESC;

SELECT region, ROUND(SUM(revenue), 2) AS revenue, ROUND(SUM(profit), 2) AS profit
FROM completed_sales
GROUP BY region
ORDER BY revenue DESC;

SELECT payment_method, ROUND(SUM(revenue), 2) AS revenue
FROM completed_sales
GROUP BY payment_method
ORDER BY revenue DESC;
