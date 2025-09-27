# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar y registrar los Blueprints (controladores)
    from .controllers.producto_controller import producto_bp
    from .controllers.cliente_controller import cliente_bp
    from .controllers.vehiculo_controller import vehiculo_bp

    app.register_blueprint(producto_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(vehiculo_bp)

    return app