import sqlite3
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "demo.db")

def regexp(expr, item):
    reg = re.compile(expr, re.IGNORECASE)
    return reg.search(item) is not None

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.create_function("REGEXP", 2, regexp)
    return conn

def init_db():
    conn = get_db()
    with open('db/schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized")

if __name__ == "__main__":
    init_db()