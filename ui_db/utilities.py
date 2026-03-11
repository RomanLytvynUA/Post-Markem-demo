import sqlite3
from .setup import get_db

def _get_configured_connection():
    """Get a connection with dictionary-like row access"""
    conn = get_db()
    conn.row_factory = sqlite3.Row 
    return conn

def execute_read_one(query, params=()):
    """
    Execute a SELECT query expecting a single result
    Return a dictionary or None
    """
    conn = _get_configured_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()

        return dict(row) if row else None
    finally:
        conn.close()

def execute_read_all(query, params=()):
    """
    Execute a SELECT query expecting multiple results.
    Return a list of dictionaries.
    """
    conn = _get_configured_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    finally:
        conn.close()