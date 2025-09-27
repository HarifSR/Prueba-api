# app/models/producto_model.py
from app.db import get_db_connection

def get_all_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductoID, Nombre, Descripcion, Precio, CategoriaID FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def get_producto_by_id(producto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos WHERE ProductoID = ?", producto_id)
    producto = cursor.fetchone()
    conn.close()
    return producto

def create_producto(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Productos (Nombre, Descripcion, Precio, CategoriaID) OUTPUT INSERTED.ProductoID VALUES (?, ?, ?, ?)"
    cursor.execute(sql, data['nombre'], data['descripcion'], data['precio'], data['categoria_id'])
    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return new_id