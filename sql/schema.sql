-- PostgreSQL-first schema. The column types are also compatible with SQLite for local validation.

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20),
    age INTEGER,
    city VARCHAR(50),
    state VARCHAR(80),
    region VARCHAR(50),
    country VARCHAR(50),
    signup_date DATE
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    cost_price NUMERIC(10, 2) NOT NULL,
    selling_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    order_year INTEGER NOT NULL,
    order_month VARCHAR(7) NOT NULL,
    order_week INTEGER NOT NULL,
    payment_method VARCHAR(30),
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    discount NUMERIC(6, 4) NOT NULL CHECK (discount >= 0),
    discount_amount NUMERIC(10, 2) NOT NULL,
    gross_revenue NUMERIC(12, 2) NOT NULL,
    revenue NUMERIC(12, 2) NOT NULL,
    cost NUMERIC(12, 2) NOT NULL,
    shipping_cost NUMERIC(10, 2) NOT NULL,
    profit NUMERIC(12, 2) NOT NULL,
    profit_margin NUMERIC(8, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_order_items_product ON order_items (product_id);
CREATE INDEX idx_products_category ON products (category, sub_category);
CREATE INDEX idx_customers_region ON customers (region, state);
