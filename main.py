from flask import Flask
from flask_cors import CORS
from src.routes import register_blueprints  # Registrar rutas desde el paquete routes
from src.database import init_db  # Inicializar la base de datos
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar CORS para manejar solicitudes del cliente
IONIC_CLIENT = os.getenv('IONIC_CLIENT')
CORS(app, resources={r"/*": {"origins": IONIC_CLIENT}})

# Inicializar la base de datos (crear tablas si no existen)
init_db()

# Registrar los blueprints (rutas)
register_blueprints(app)

# Configuración adicional (por ejemplo, carpeta de subidas)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

# Ejecutar el servidor
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
