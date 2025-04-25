from flask import Flask
from flask_cors import CORS
from src.routes import register_blueprints  # Registrar rutas desde el paquete routes
from src.database import init_db  # Inicializar la base de datos
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar CORS para manejar solicitudes del cliente
IONIC_CLIENT = os.getenv('IONIC_CLIENT')
CORS(app, resources={r"/*": {"origins": IONIC_CLIENT}})
# CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar la base de datos (crear tablas si no existen)
init_db()


# Configuración adicional (por ejemplo, carpeta de subidas)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

socketio = SocketIO(app, cors_allowed_origins=IONIC_CLIENT)
# socketio = SocketIO(app, cors_allowed_origins="*")

# Registrar los blueprints (rutas)
register_blueprints(app, socketio)

# Ejecutar el servidor
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)