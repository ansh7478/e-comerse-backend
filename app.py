from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE_NAME = "shop.db"


# Connect to SQLite database
def get_database_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# Create required database tables
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

    connection.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    connection.commit()
    connection.close()


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to PyShop E-Commerce REST API"
    }), 200


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


# Get one product
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


# Add a product
@app.route("/products", methods=["POST"])
def add_product():
    product_data = request.get_json()

    if product_data is None:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    required_fields = ["name", "category", "price", "stock"]

    for field in required_fields:
        if field not in product_data:
            return jsonify({
                "error": field + " is required"
            }), 400

    if product_data["price"] < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if product_data["stock"] < 0:
        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    connection = get_database_connection()

    cursor = connection.execute(
        """
        INSERT INTO products (name, category, price, stock)
        VALUES (?, ?, ?, ?)
        """,
        (
            product_data["name"],
            product_data["category"],
            product_data["price"],
            product_data["stock"]
        )
    )

    connection.commit()
    product_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "message": "Product added successfully",
        "product_id": product_id
    }), 201


# Update a product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product_data = request.get_json()

    if product_data is None:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    required_fields = ["name", "category", "price", "stock"]

    for field in required_fields:
        if field not in product_data:
            return jsonify({
                "error": field + " is required"
            }), 400

    if product_data["price"] < 0 or product_data["stock"] < 0:
        return jsonify({
            "error": "Price and stock cannot be negative"
        }), 400

    connection = get_database_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    connection.execute(
        """
        UPDATE products
        SET name = ?, category = ?, price = ?, stock = ?
        WHERE id = ?
        """,
        (
            product_data["name"],
            product_data["category"],
            product_data["price"],
            product_data["stock"],
            product_id
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product updated successfully"
    }), 200


# Delete a product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    connection = get_database_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200


# Add product to cart
@app.route("/cart", methods=["POST"])
def add_to_cart():
    cart_data = request.get_json()

    if cart_data is None:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    if "product_id" not in cart_data or "quantity" not in cart_data:
        return jsonify({
            "error": "Product ID and quantity are required"
        }), 400

    if cart_data["quantity"] <= 0:
        return jsonify({
            "error": "Quantity must be greater than zero"
        }), 400

    connection = get_database_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (cart_data["product_id"],)
    ).fetchone()

    if product is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    if cart_data["quantity"] > product["stock"]:
        connection.close()

        return jsonify({
            "error": "Not enough stock available"
        }), 400

    cursor = connection.execute(
        """
        INSERT INTO cart (product_id, quantity)
        VALUES (?, ?)
        """,
        (
            cart_data["product_id"],
            cart_data["quantity"]
        )
    )

    connection.commit()
    cart_item_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "message": "Product added to cart",
        "cart_item_id": cart_item_id
    }), 201


# View cart
@app.route("/cart", methods=["GET"])
def get_cart():
    connection = get_database_connection()

    cart_items = connection.execute("""
        SELECT
            cart.id,
            products.name,
            products.price,
            cart.quantity,
            products.price * cart.quantity AS total
        FROM cart
        JOIN products ON cart.product_id = products.id
    """).fetchall()

    connection.close()

    cart_list = []

    for item in cart_items:
        cart_list.append({
            "cart_item_id": item["id"],
            "product_name": item["name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "total": item["total"]
        })

    return jsonify(cart_list), 200


# Delete item from cart
@app.route("/cart/<int:cart_item_id>", methods=["DELETE"])
def delete_cart_item(cart_item_id):
    connection = get_database_connection()

    cart_item = connection.execute(
        "SELECT * FROM cart WHERE id = ?",
        (cart_item_id,)
    ).fetchone()

    if cart_item is None:
        connection.close()

        return jsonify({
            "error": "Cart item not found"
        }), 404

    connection.execute(
        "DELETE FROM cart WHERE id = ?",
        (cart_item_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Cart item deleted successfully"
    }), 200


if __name__ == "__main__":
    create_database()
    app.run(debug=True)