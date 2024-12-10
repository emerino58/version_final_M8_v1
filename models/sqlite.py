import sqlite3
import os

def get_connection():
    """Establece y devuelve una conexión a la base de datos SQLite."""

    # Construir la ruta relativa al archivo usuarios.csv desde el archivo login.py
    sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'chile.db')

    # Convertir a ruta absoluta
    sqlite_path = os.path.abspath(sqlite_path)
    conn = sqlite3.connect(sqlite_path)
    return conn

def execute_query(query, params=()):
    """Ejecuta una consulta y devuelve los resultados si corresponde."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results
