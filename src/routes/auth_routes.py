from flask import Blueprint, request, jsonify
from src.services.auth_service import register_user, authenticate_user, verify_token

auth_bp = Blueprint('auth', __name__)

# Ruta para registrar usuarios
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(error="Username y password son requeridos"), 400

    response = register_user(username, password)
    return jsonify(response), 201 if "message" in response else 400

# Ruta para inicio de sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(error="Username y password son requeridos"), 400

    response = authenticate_user(username, password)
    return jsonify(response), 200 if "message" in response else 401

# Ruta para verificar token
@auth_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify(error="Token es requerido"), 400

    response = verify_token(token)
    return jsonify(response), 200 if "id" in response else 401
