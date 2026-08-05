# Product Inventory System

A simple, self-contained web application for managing product inventory, built with **Flask** and **SQLite**.

## Features

- 📊 **Dashboard** — total products, units in stock, inventory value, and low-stock alerts
- 📋 **View Products** — table of all products with edit/delete actions
- ➕ **Add Product** — form to add a new product to inventory
- ✏️ **Edit Product** — update details of an existing product
- 🔍 **Search Products** — search by name, category, or supplier
- 🗑️ **Delete Product** — remove a product with a confirmation prompt

## Project Structure

```
ProductInventorySystem/
│
├── app.py                     # Flask application & routes
├── db.py                      # Database access layer (SQLite)
├── requirements.txt           # Python dependencies
├── product_inventory.sql      # Database schema + seed data
│
├── static/
│   ├── css/
│   │     └── style.css        # App styling
│   └── images/                # (optional) product/UI images
│
├── templates/
│   ├── index.html              # Dashboard
│   ├── add_product.html        # Add product form
│   ├── view_products.html      # Product listing
│   ├── edit_product.html       # Edit product form
│   └── search_product.html     # Search page
│
└── README.md
```

## Setup & Installation

1. **Clone / copy the project folder**, then move into it:
   ```bash
   cd ProductInventorySystem
   ```

2. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

5. Open your browser to **http://127.0.0.1:5000**

The SQLite database (`product_inventory.db`) is created automatically on first run using the schema and seed data in `product_inventory.sql`. No separate database server is required.

## Resetting the Database

To wipe the database and reseed it from scratch, delete `product_inventory.db` and restart the app:

```bash
rm product_inventory.db
python app.py
```

## Using MySQL/PostgreSQL Instead of SQLite

`product_inventory.sql` uses standard SQL and can be adapted for MySQL or PostgreSQL with minor tweaks (e.g. `INTEGER PRIMARY KEY AUTOINCREMENT` → `INT AUTO_INCREMENT PRIMARY KEY` for MySQL, or `SERIAL PRIMARY KEY` for PostgreSQL). Only `db.py` needs to change — swap the `sqlite3` connection logic for `mysql-connector-python` or `psycopg2`, and update `requirements.txt` accordingly. `app.py` and the templates require no changes since they only call the functions defined in `db.py`.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Python's built-in `sqlite3` module)
- **Frontend:** HTML, Jinja2 templates, custom CSS (no JS framework required)

## License

This project is provided as-is for educational and demonstration purposes.
