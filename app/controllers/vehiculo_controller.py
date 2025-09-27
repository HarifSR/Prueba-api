# app/controllers/vehiculo_controller.py
from flask import Blueprint, jsonify
from app.models.vehiculo_model import get_all_vehiculos

vehiculo_bp = Blueprint('vehiculo', __name__)

@vehiculo_bp.route('/vehiculos', methods=['GET'])
def find_all():
    try:
        vehiculos = get_all_vehiculos()
        return jsonify([{
            "id": row.id, "modelo": row.modelo,
            "marca": row.marca, "linea": row.linea
        } for row in vehiculos])
    except Exception as e:
        return jsonify({"message": "Error en el servidor", "error": str(e)}), 500