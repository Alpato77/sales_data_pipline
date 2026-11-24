\connect ecommerce_sales

CREATE TABLE IF NOT EXISTS sales (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    order_date DATE NOT NULL,
    status TEXT,
    total_amount NUMERIC(12, 2) NOT NULL
);
