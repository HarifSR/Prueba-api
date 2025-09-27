# app/models/cliente_model.py
from app.db import get_db_connection

def get_all_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ClienteID, Nombre, Apellido, Email, FechaRegistro FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def create_cliente(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Clientes (Nombre, Apellido, Email) OUTPUT INSERTED.ClienteID VALUES (?, ?, ?)"
    cursor.execute(sql, data['nombre'], data['apellido'], data['email'])
    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return new_id