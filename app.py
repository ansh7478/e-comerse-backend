from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DATABASE_NAME = "shop.db"


# Connect to SQLite database
def get_database_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# Create products table
def create_database():
    connection = get_database_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to PyShop E-Commerce REST API"
    })

# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    connection = get_database_connection()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    product_list = []

    for product in products:
        product_list.append({
            "id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "stock": product["stock"]
        })

    return jsonify(product_list), 200


# Get one product by ID
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    connection = get_database_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify({
        "id": product["id"],
        "name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "stock": product["stock"]
    }), 200

if __name__ == "__main__":
    create_database()
    app.run(debug=True)