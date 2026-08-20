WITH completed_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.sub_category,
        oi.quantity,
        oi.revenue,
        oi.profit,
        oi.profit_margin
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
)
SELECT
    product_id,
    product_name,
    category,
    ROUND(SUM(revenue), 2) AS revenue
FROM completed_sales
GROUP BY product_id, product_name, category
ORDER BY revenue DESC
LIMIT 10;

SELECT
    product_id,
    product_name,
    category,
    ROUND(SUM(profit), 2) AS profit
FROM completed_sales
GROUP BY product_id, product_name, category
ORDER BY profit DESC
LIMIT 10;

SELECT
    product_id,
    product_name,
    category,
    SUM(quantity) AS units_sold
FROM completed_sales
GROUP BY product_id, product_name, category
ORDER BY units_sold DESC
LIMIT 10;

SELECT
    product_id,
    product_name,
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM completed_sales
GROUP BY product_id, product_name, category
ORDER BY revenue ASC
LIMIT 10;

SELECT
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / NULLIF(SUM(revenue), 0)) * 100, 2) AS profit_margin_pct
FROM completed_sales
GROUP BY category
ORDER BY profit DESC;

SELECT
    product_id,
    product_name,
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND((SUM(profit) / NULLIF(SUM(revenue), 0)) * 100, 2) AS profit_margin_pct
FROM completed_sales
GROUP BY product_id, product_name, category
HAVING SUM(revenue) > (
    SELECT AVG(product_revenue)
    FROM (
        SELECT SUM(revenue) AS product_revenue
        FROM completed_sales
        GROUP BY product_id
    ) revenue_benchmark
)
AND (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100 < 20
ORDER BY revenue DESC;
