# app/controllers/cliente_controller.py
from flask import Blueprint, jsonify, request
from app.models.cliente_model import get_all_clientes, create_cliente

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def find_all():
    try:
        clientes = get_all_clientes()
        return jsonify([{
            "cliente_id": row.ClienteID, "nombre": row.Nombre, "apellido": row.Apellido,
            "email": row.Email, "fecha_registro": row.FechaRegistro.isoformat()
        } for row in clientes])
    except Exception as e:
        return jsonify({"message": "Error en el servidor", "error": str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def add_cliente():
    try:
        data = request.get_json()
        new_id = create_cliente(data)
        return jsonify({"message": "Cliente creado con éxito", "cliente_id": new_id}), 201
    except Exception as e:
        return jsonify({"message": "Error en el servidor", "error": str(e)}), 500