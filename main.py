from flask import Flask, jsonify, request
import pyodbc
from flasgger import Swagger # <--- 1. IMPORTAR SWAGGER

app = Flask(__name__)
swagger = Swagger(app) # <--- 2. INICIALIZAR SWAGGER

# --- Configuración de la conexión a la base de datos ---
server = 'svr-sql-ctezo.southcentralus.cloudapp.azure.com'
database = 'db_DesaWebDevUMG'
username = 'usr_DesaWebDevUMG'
password = '!ngGuast@360'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


def get_db_connection():
    """Crea y retorna una conexión a la base de datos."""
    return pyodbc.connect(connection_string)

# --- Rutas para la tabla PRODUCTOS ---

@app.route('/productos', methods=['GET'])
def get_productos():
    """Obtiene todos los productos."""
    productos = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Usamos los nombres de columna correctos de tu tabla
        cursor.execute("SELECT ProductoID, Nombre, Descripcion, Precio, CategoriaID FROM Productos")
        rows = cursor.fetchall()
        for row in rows:
            productos.append({
                "producto_id": row.ProductoID,
                "nombre": row.Nombre,
                "descripcion": row.Descripcion,
                "precio": float(row.Precio), # Convertimos el decimal a float para JSON
                "categoria_id": row.CategoriaID
            })
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500
    return jsonify(productos)

@app.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    """Obtiene un producto por su ID."""
    producto = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ProductoID, Nombre, Descripcion, Precio, CategoriaID FROM Productos WHERE ProductoID = ?", producto_id)
        row = cursor.fetchone()
        if row:
            producto = {
                "producto_id": row.ProductoID,
                "nombre": row.Nombre,
                "descripcion": row.Descripcion,
                "precio": float(row.Precio),
                "categoria_id": row.CategoriaID
            }
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500
    
    if producto:
        return jsonify(producto)
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

@app.route('/productos', methods=['POST'])
def add_producto():
    """Agrega un nuevo producto."""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO Productos (Nombre, Descripcion, Precio, CategoriaID) 
                 OUTPUT INSERTED.ProductoID 
                 VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, data['nombre'], data['descripcion'], data['precio'], data['categoria_id'])
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"message": "Producto creado con éxito", "producto_id": new_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor o datos inválidos"}), 500
    
# --- Rutas para la tabla CLIENTES ---

@app.route('/clientes', methods=['GET'])
def get_clientes():
    """
    Obtener la lista completa de clientes.
    Esta ruta devuelve un arreglo con todos los clientes en la base de datos.
    ---
    responses:
      200:
        description: Una lista de todos los clientes.
        schema:
          type: array
          items:
            type: object
            properties:
              cliente_id:
                type: integer
              nombre:
                type: string
              apellido:
                type: string
              email:
                type: string
              fecha_registro:
                type: string
                format: date-time
      500:
        description: Error interno del servidor.
    """
    # ... (El código de la función no cambia)
    clientes = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ClienteID, Nombre, Apellido, Email, FechaRegistro FROM Clientes")
        rows = cursor.fetchall()
        for row in rows:
            clientes.append({
                "cliente_id": row.ClienteID,
                "nombre": row.Nombre,
                "apellido": row.Apellido,
                "email": row.Email,
                "fecha_registro": row.FechaRegistro.isoformat()
            })
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500
    return jsonify(clientes)

@app.route('/clientes', methods=['POST'])
def add_cliente():
    """
    Crear un nuevo cliente.
    Agrega un nuevo cliente a la base de datos con la información proporcionada.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre del cliente.
              example: "Ana"
            apellido:
              type: string
              description: Apellido del cliente.
              example: "Solis"
            email:
              type: string
              description: Correo electrónico único del cliente.
              example: "ana.s@correo.com"
    responses:
      201:
        description: Cliente creado exitosamente.
      500:
        description: Error interno del servidor o datos inválidos.
    """
    # ... (El código de la función no cambia)
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO Clientes (Nombre, Apellido, Email) OUTPUT INSERTED.ClienteID VALUES (?, ?, ?)"
        cursor.execute(sql, data['nombre'], data['apellido'], data['email'])
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"message": "Cliente creado con éxito", "cliente_id": new_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor o datos inválidos"}), 500
# --- Rutas para la tabla VEHICULOS ---

@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    """Obtiene todos los vehículos."""
    vehiculos = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, modelo, marca, linea FROM vehiculos")
        rows = cursor.fetchall()
        for row in rows:
            vehiculos.append({
                "id": row.id,
                "modelo": row.modelo,
                "marca": row.marca,
                "linea": row.linea
            })
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500
    return jsonify(vehiculos)


if __name__ == '__main__':
    app.run(debug=False)