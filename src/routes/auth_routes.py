from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Lógica para registrar usuarios
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Guardar en la base de datos (placeholder)
    return jsonify(message=f"Usuario {username} registrado exitosamente"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    # Lógica para inicio de sesión
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Verificar credenciales en la base de datos (placeholder)
    return jsonify(message=f"Usuario {username} inició sesión"), 200
