-- ============================================================
-- Product Inventory System - Database Schema
-- ============================================================
-- This schema works with SQLite (used by default in db.py) and
-- is standard enough to be adapted to MySQL/PostgreSQL with only
-- minor type changes (e.g. INTEGER PRIMARY KEY AUTOINCREMENT ->
-- INT AUTO_INCREMENT PRIMARY KEY for MySQL).
-- ============================================================

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    category      TEXT NOT NULL,
    quantity      INTEGER NOT NULL DEFAULT 0,
    price         REAL NOT NULL DEFAULT 0.0,
    supplier      TEXT,
    description   TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample seed data
INSERT INTO products (name, category, quantity, price, supplier, description) VALUES
('Wireless Mouse', 'Electronics', 150, 19.99, 'TechSupply Co.', 'Ergonomic wireless mouse with USB receiver'),
('Office Chair', 'Furniture', 40, 89.50, 'Comfort Furnishings', 'Adjustable height office chair with lumbar support'),
('Notebook Pack (5x)', 'Stationery', 300, 6.75, 'PaperWorks Ltd.', 'Pack of 5 ruled notebooks, 100 pages each'),
('LED Desk Lamp', 'Electronics', 75, 24.99, 'BrightLite Inc.', 'Adjustable LED desk lamp with USB charging port'),
('Water Bottle 1L', 'Accessories', 200, 9.99, 'HydroGear', 'BPA-free reusable water bottle');
