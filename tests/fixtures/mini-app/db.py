import sqlite3

def connect(path="app.db"):
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    return c

def init(c):
    c.executescript("""
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
    CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL, created_at TEXT);
    CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, customer_id INTEGER, subject TEXT, body TEXT);
    CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
    """)
    c.commit()
