"""
db.py
-----
Database access layer for the Product Inventory System.

Uses SQLite for a fully self-contained, zero-configuration setup.
The database file (product_inventory.db) is created automatically
from product_inventory.sql the first time the app runs.

If you'd rather use MySQL/PostgreSQL in production, swap out the
`get_connection()` function below for your driver of choice
(e.g. mysql-connector-python or psycopg2) - the rest of the app
only relies on the functions defined in this file, so no changes
are needed elsewhere.
"""

import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "product_inventory.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "product_inventory.sql")


def get_connection():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(force=False):
    """
    Initialize the database from the schema file.

    If the database file doesn't exist yet, it will be created and
    seeded. Pass force=True to drop and recreate it even if it
    already exists.
    """
    if force and os.path.exists(DATABASE):
        os.remove(DATABASE)

    if not os.path.exists(DATABASE):
        conn = get_connection()
        with open(SCHEMA_FILE, "r") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        conn.close()
        print(f"Initialized database at {DATABASE}")


# ---------------------------------------------------------------
# CRUD helper functions
# ---------------------------------------------------------------

def get_all_products():
    conn = get_connection()
    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return products


def get_product_by_id(product_id):
    conn = get_connection()
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()
    return product


def add_product(name, category, quantity, price, supplier, description):
    conn = get_connection()
    conn.execute(
        """INSERT INTO products (name, category, quantity, price, supplier, description)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (name, category, quantity, price, supplier, description),
    )
    conn.commit()
    conn.close()


def update_product(product_id, name, category, quantity, price, supplier, description):
    conn = get_connection()
    conn.execute(
        """UPDATE products
           SET name = ?, category = ?, quantity = ?, price = ?,
               supplier = ?, description = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (name, category, quantity, price, supplier, description, product_id),
    )
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def search_products(query):
    conn = get_connection()
    like_query = f"%{query}%"
    products = conn.execute(
        """SELECT * FROM products
           WHERE name LIKE ? OR category LIKE ? OR supplier LIKE ?
           ORDER BY id DESC""",
        (like_query, like_query, like_query),
    ).fetchall()
    conn.close()
    return products


def get_low_stock_products(threshold=20):
    conn = get_connection()
    products = conn.execute(
        "SELECT * FROM products WHERE quantity <= ? ORDER BY quantity ASC",
        (threshold,),
    ).fetchall()
    conn.close()
    return products
