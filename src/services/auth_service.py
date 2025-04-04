import jwt
import datetime
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import insert_user, get_user_by_username

load_dotenv()

# Clave secreta para firmar los tokens (obtenida desde .env)
SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')

def register_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        insert_user(username, password_hash)
        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        return {"error": str(e)}

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user:
        if check_password_hash(user['password_hash'], password):
            # Generar un token JWT
            token = jwt.encode({
                'id': user['id'],
                'username': user['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token válido por 1 hora
            }, SECRET_KEY, algorithm='HS256')

            return {"message": "Autenticación exitosa", "token": token}
        else:
            return {"error": "Contraseña incorrecta"}
    return {"error": "Usuario no encontrado"}

def verify_token(token):
    # Eliminar el prefijo "Bearer " del token
    new_token = token.replace("Bearer ", "") if "Bearer " in token else token
    try:
        # Decodificar el token para verificar su validez
        decoded = jwt.decode(new_token, SECRET_KEY, algorithms=['HS256'])
        return decoded  # Contiene la información del usuario
    except jwt.ExpiredSignatureError:
        return {"error": "El token ha expirado"}
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}
