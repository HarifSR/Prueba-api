# app/models/vehiculo_model.py
from app.db import get_db_connection

def get_all_vehiculos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, modelo, marca, linea FROM vehiculos")
    vehiculos = cursor.fetchall()
    conn.close()
    return vehiculos