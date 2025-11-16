import sqlite3
import hashlib
import json
from contextlib import contextmanager
from .data_models import User, Product, Order, OrderItem
import os

# --- Database Path ---
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(DB_DIR, "cupcake_store.db")

# --- Context Manager for DB Connection ---
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- Setup ---
def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
        except sqlite3.OperationalError:
            pass # Column already exists
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, is_admin BOOLEAN, status TEXT DEFAULT 'active')")
        cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL, stock INTEGER, flavor TEXT, image_url TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, order_date TEXT, status TEXT, total_price REAL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER, price_per_unit REAL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS store_settings (key TEXT PRIMARY KEY, value TEXT)")
        cursor.execute("INSERT OR IGNORE INTO store_settings (key, value) VALUES (?, ?)", ('payment_methods', json.dumps(['Credit Card', 'PayPal', 'Bank Transfer'])))
        conn.commit()

# --- Hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Reusable Connection Functions ---
def _execute_query(query, params=(), fetch=None, conn=None):
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch == 'one': return cursor.fetchone()
        if fetch == 'all': return cursor.fetchall()
        return cursor
    else:
        with get_db_connection() as new_conn:
            cursor = new_conn.cursor()
            cursor.execute(query, params)
            if fetch == 'one': return cursor.fetchone()
            if fetch == 'all': return cursor.fetchall()
            new_conn.commit()
            return cursor

# --- Product CRUD ---
def get_product_by_id(product_id: int, conn=None):
    row = _execute_query("SELECT * FROM products WHERE id = ?", (product_id,), fetch='one', conn=conn)
    return Product(**row) if row else None

def update_product_stock(product_id: int, quantity_change: int, conn=None):
    _execute_query("UPDATE products SET stock = stock + ? WHERE id = ?", (quantity_change, product_id), conn=conn)

# --- Order CRUD ---
def create_order(order: Order, cart_items: list):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, total_price, status, order_date) VALUES (?, ?, ?, datetime('now'))", (order.user_id, order.total_price, order.status))
        order_id = cursor.lastrowid
        for item in cart_items:
            product = get_product_by_id(item['product_id'], conn=conn)
            if product:
                cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)", (order_id, item['product_id'], item['quantity'], product.price))
                update_product_stock(item['product_id'], -item['quantity'], conn=conn)
        conn.commit()
        return order_id

def cancel_order(order_id: int):
    with get_db_connection() as conn:
        order = _execute_query("SELECT * FROM orders WHERE id = ?", (order_id,), fetch='one', conn=conn)
        if not order:
            return False # Order not found

        if order['status'] == 'Pending':
            _execute_query("UPDATE orders SET status = 'Cancelled' WHERE id = ?", (order_id,), conn=conn)
            items = get_order_items(order_id, conn=conn)
            for item in items:
                update_product_stock(item.product_id, item.quantity, conn=conn) # Restore stock
            conn.commit()
            return True
        return False # Not pending, cannot cancel

def get_order_items(order_id: int, conn=None):
    rows = _execute_query("SELECT * FROM order_items WHERE order_id = ?", (order_id,), fetch='all', conn=conn)
    return [OrderItem(**row) for row in rows]

# --- User CRUD ---
def add_user(user: User):
    _execute_query("INSERT INTO users (name, email, password, is_admin, status) VALUES (?, ?, ?, ?, ?)", (user.name, user.email, hash_password(user.password), user.is_admin, user.status))

def get_user_by_email(email: str):
    row = _execute_query("SELECT * FROM users WHERE email = ?", (email,), fetch='one')
    return User(**row) if row else None

def get_all_users():
    rows = _execute_query("SELECT * FROM users", fetch='all')
    return [User(**row) for row in rows]

def update_user(user: User):
    if user.password:
        _execute_query("UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?", (user.name, user.email, hash_password(user.password), user.id))
    else:
        _execute_query("UPDATE users SET name = ?, email = ? WHERE id = ?", (user.name, user.email, user.id))

def update_user_admin_status(user_id: int, is_admin: bool):
    _execute_query("UPDATE users SET is_admin = ? WHERE id = ?", (is_admin, user_id))

def update_user_status(user_id: int, status: str):
    _execute_query("UPDATE users SET status = ? WHERE id = ?", (status, user_id))

# --- Product Management ---
def add_product(product: Product):
    _execute_query("INSERT INTO products (name, description, price, stock, flavor, image_url) VALUES (?, ?, ?, ?, ?, ?)", (product.name, product.description, product.price, product.stock, product.flavor, product.image_url))

def get_all_products(flavor_filter=None):
    query = "SELECT * FROM products"
    params = ()
    if flavor_filter and flavor_filter != "All":
        query += " WHERE flavor = ?"
        params = (flavor_filter,)
    rows = _execute_query(query, params, fetch='all')
    return [Product(**row) for row in rows]

def get_flavors():
    rows = _execute_query("SELECT DISTINCT flavor FROM products WHERE flavor IS NOT NULL AND flavor != ''", fetch='all')
    return [row['flavor'] for row in rows]

def set_product_stock(product_id: int, new_stock: int):
    _execute_query("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))

def update_product(product: Product):
    _execute_query("UPDATE products SET name = ?, description = ?, price = ?, stock = ?, flavor = ?, image_url = ? WHERE id = ?", (product.name, product.description, product.price, product.stock, product.flavor, product.image_url, product.id))

def delete_product(product_id: int):
    _execute_query("DELETE FROM products WHERE id = ?", (product_id,))

# --- Order Management ---
def get_orders_by_user(user_id: int):
    rows = _execute_query("SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC", (user_id,), fetch='all')
    return [Order(**row) for row in rows]

def get_all_orders():
    rows = _execute_query("SELECT * FROM orders ORDER BY order_date DESC", fetch='all')
    return [Order(**row) for row in rows]

def update_order_status(order_id: int, status: str):
    _execute_query("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))

# --- Store Settings ---
def get_store_settings():
    rows = _execute_query("SELECT key, value FROM store_settings", fetch='all')
    return {row['key']: json.loads(row['value']) for row in rows}

def update_store_setting(key: str, value: list):
    _execute_query("UPDATE store_settings SET value = ? WHERE key = ?", (json.dumps(value), key))
