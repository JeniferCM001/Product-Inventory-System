"""
app.py
------
Main Flask application for the Product Inventory System.

Routes:
    GET  /                     -> Home / dashboard
    GET  /products              -> View all products
    GET  /products/add          -> Show add-product form
    POST /products/add          -> Handle add-product submission
    GET  /products/edit/<id>    -> Show edit-product form
    POST /products/edit/<id>    -> Handle edit-product submission
    POST /products/delete/<id>  -> Delete a product
    GET  /products/search       -> Search-product form + results
"""

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
import db

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # needed for flash messages / sessions

# Hardcoded accounts, keyed by username.
# NOTE: for a real deployment, replace this with a proper user table and
# hashed passwords (e.g. werkzeug.security.generate_password_hash).
# role "staff" -> full access (view, add, edit, delete)
# role "user"  -> read-only access (dashboard, browse, search)
USERS = {
    "admin": {"password": "123@product", "role": "staff"},
    "user": {"password": "user@123", "role": "user"},
}


def login_required(view_func):
    """Redirect to the login page if the user isn't authenticated."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        return view_func(*args, **kwargs)
    return wrapped


def staff_required(view_func):
    """Block access unless the logged-in account has the 'staff' role."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        if session.get("role") != "staff":
            flash("That action needs staff access.", "error")
            return redirect(url_for("view_products"))
        return view_func(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_user_context():
    """Make the current role available to every template."""
    return {
        "current_username": session.get("username"),
        "current_role": session.get("role"),
        "is_staff": session.get("role") == "staff",
    }


@app.before_request
def ensure_db():
    db.init_db()


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        account = USERS.get(username)

        if account and password == account["password"]:
            session["logged_in"] = True
            session["username"] = username
            session["role"] = account["role"]
            flash("Logged in successfully.", "success")
            next_url = request.form.get("next") or url_for("index")
            return redirect(next_url)

        flash("Invalid username or password.", "error")
        return render_template("login.html", username=username)

    return render_template("login.html", username="")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    products = db.get_all_products()
    total_products = len(products)
    total_quantity = sum(p["quantity"] for p in products) if products else 0
    total_value = sum(p["quantity"] * p["price"] for p in products) if products else 0
    low_stock = db.get_low_stock_products(threshold=20)

    return render_template(
        "index.html",
        total_products=total_products,
        total_quantity=total_quantity,
        total_value=total_value,
        low_stock=low_stock,
    )


@app.route("/products")
@login_required
def view_products():
    products = db.get_all_products()
    return render_template("view_products.html", products=products)


@app.route("/products/add", methods=["GET", "POST"])
@staff_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        quantity = request.form.get("quantity", "0").strip()
        price = request.form.get("price", "0").strip()
        supplier = request.form.get("supplier", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not category:
            flash("Name and category are required.", "error")
            return render_template("add_product.html", form_data=request.form)

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            flash("Quantity must be a whole number and price must be a number.", "error")
            return render_template("add_product.html", form_data=request.form)

        db.add_product(name, category, quantity, price, supplier, description)
        flash(f'Product "{name}" added successfully.', "success")
        return redirect(url_for("view_products"))

    return render_template("add_product.html", form_data={})


@app.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@staff_required
def edit_product(product_id):
    product = db.get_product_by_id(product_id)
    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("view_products"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        quantity = request.form.get("quantity", "0").strip()
        price = request.form.get("price", "0").strip()
        supplier = request.form.get("supplier", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not category:
            flash("Name and category are required.", "error")
            return render_template("edit_product.html", product=product)

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            flash("Quantity must be a whole number and price must be a number.", "error")
            return render_template("edit_product.html", product=product)

        db.update_product(product_id, name, category, quantity, price, supplier, description)
        flash(f'Product "{name}" updated successfully.', "success")
        return redirect(url_for("view_products"))

    return render_template("edit_product.html", product=product)


@app.route("/products/delete/<int:product_id>", methods=["POST"])
@staff_required
def delete_product(product_id):
    product = db.get_product_by_id(product_id)
    if product is None:
        flash("Product not found.", "error")
    else:
        db.delete_product(product_id)
        flash(f'Product "{product["name"]}" deleted.', "success")
    return redirect(url_for("view_products"))


@app.route("/products/search", methods=["GET"])
@login_required
def search_product():
    query = request.args.get("q", "").strip()
    results = db.search_products(query) if query else []
    return render_template("search_product.html", query=query, results=results)


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
