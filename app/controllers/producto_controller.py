# app/controllers/producto_controller.py
from flask import Blueprint, jsonify, request
from app.models.producto_model import get_all_productos, get_producto_by_id, create_producto

# Creamos un Blueprint para organizar las rutas
producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/productos', methods=['GET'])
def find_all():
    try:
        productos = get_all_productos()
        return jsonify([{
            "producto_id": row.ProductoID, "nombre": row.Nombre, "descripcion": row.Descripcion,
            "precio": float(row.Precio), "categoria_id": row.CategoriaID
        } for row in productos])
    except Exception as e:
        return jsonify({"message": "Error en el servidor", "error": str(e)}), 500

@producto_bp.route('/productos/<int:producto_id>', methods=['GET'])
def find_one(producto_id):
    try:
        producto = get_producto_by_id(producto_id)
        if producto:
            return jsonify({
                "producto_id": producto.ProductoID, "nombre": producto.Nombre,
                "descripcion": producto.Descripcion, "precio": float(producto.Precio),
                "categoria_id": producto.CategoriaID
            })
        return jsonify({"message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Error en el servidor", "error": str(e)}), 500

@producto_bp.route('/productos', methods=['POST'])
def add_producto():
    try:
        data = request.get_json()
        new_id = create_producto(data)
        return jsonify({"message": "Producto creado con éxito", "producto_id": new_id}), 201
    except Exception as e:
        return jsonify({"message": "Error en el servidor", "error": str(e)}), 500