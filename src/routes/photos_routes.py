from flask import Blueprint, request, jsonify
from src.services.photos_service import process_and_save_image, get_latests_images, show_image

# Crear el Blueprint para las rutas de imágenes
photos_bp = Blueprint('photos', __name__)

# Endpoint para subir un archivo y analizarlo
@photos_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    try:
        result = process_and_save_image(file)
        return jsonify(message='File successfully uploaded', data=result), 200
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return jsonify(error=f"Error al procesar la imagen: {e}"), 500

# Endpoint para obtener las últimas 20 imágenes
@photos_bp.route('/latests-images', methods=['GET'])
def get_latests():
    try:
        images = get_latests_images(limit=20)
        return jsonify(images), 200
    except Exception as e:
        print(f"Error al obtener las imágenes: {e}")
        return jsonify(error=f"Error al obtener las imágenes: {e}"), 500

# Endpoint para servir imágenes desde la carpeta de almacenamiento
@photos_bp.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    try:
        return show_image(filename)
    except Exception as e:
        print(f"Error al servir la imagen: {e}")
        return jsonify(error=f"Error al servir la imagen: {e}"), 404
