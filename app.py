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


if __name__ == "__main__":
    create_database()
    app.run(debug=True)