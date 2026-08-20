-- Duplicate and null checks
SELECT order_id, COUNT(*) AS duplicate_order_headers
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT order_id, product_id, COUNT(*) AS duplicate_order_lines
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS missing_customer_ids
FROM orders
WHERE customer_id IS NULL;

SELECT COUNT(*) AS missing_product_ids
FROM order_items
WHERE product_id IS NULL;

SELECT COUNT(*) AS invalid_unit_prices
FROM order_items
WHERE unit_price < 0;

SELECT COUNT(*) AS invalid_quantities
FROM order_items
WHERE quantity < 0;

SELECT COUNT(*) AS invalid_order_dates
FROM orders
WHERE order_date IS NULL;

SELECT status, COUNT(*) AS orders
FROM orders
GROUP BY status
ORDER BY orders DESC;

-- Referential integrity checks
SELECT COUNT(*) AS orphan_orders
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS orphan_order_items_to_orders
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

SELECT COUNT(*) AS orphan_order_items_to_products
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;
