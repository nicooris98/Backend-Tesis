from datetime import datetime
import os
from src.services.opencv_service import detect_person
from src.database import insert_photo, get_latest_photos, get_photos_paginated
from flask import send_from_directory

# Cargar la clave desde .env
CAMERA_SECRET_KEY = os.getenv('CAMERA_SECRET_KEY')

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
IP = os.getenv('IP')
PORT = os.getenv('PORT', '3000')

def save_file(file):
    """
    Guarda un archivo en la carpeta de uploads y genera un nombre único basado en el timestamp.

    Args:
        file: Archivo recibido desde la solicitud HTTP.

    Returns:
        tuple: (filename, filepath, timestamp) que corresponden al nombre del archivo,
               la ruta completa donde fue guardado, y el timestamp actual.
    """
    timestamp = datetime.now()
    date_str = timestamp.strftime("%Y%m%d%H%M%S")
    extension = os.path.splitext(file.filename)[1]
    filename = f"{date_str}{extension}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Crear carpeta si no existe
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Guardar el archivo
    file.save(filepath)

    return filename, filepath, timestamp

def process_and_save_image(file):
    """
    Guarda el archivo, analiza la imagen con OpenCV, y registra los datos en la base de datos.

    Args:
        file: Archivo recibido desde la solicitud HTTP.

    Returns:
        dict: Datos relevantes sobre el archivo procesado, incluido si se detectó una persona.
    """
    # Guardar archivo y obtener información
    filename, filepath, timestamp = save_file(file)

    # Detectar personas en la imagen
    person_detected = detect_person(filepath)
    # print(person_detected)

    # Guardar los datos en la base de datos
    insert_photo(filename, filepath, timestamp, person_detected)

    return {
        'filename': filename,
        'filepath': filepath,
        'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'person_detected': person_detected
    }

def get_latests_images(limit=20):
    """
    Obtiene las últimas imágenes almacenadas desde la base de datos.

    Args:
        limit: Número máximo de imágenes a recuperar.

    Returns:
        list: Lista de imágenes con sus detalles.
    """
    rows = get_latest_photos(limit)
    return [
        {
            'filename': row['filename'],
            'url': f"http://{IP}:{PORT}/photos/uploads/{row['filename']}",
            'timestamp': row['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            'personDetected': row['person_detected']
        }
        for row in rows
    ]

def show_image(filename):
    """
    Devuelve una imagen desde la carpeta de almacenamiento.

    Args:
        filename (str): Nombre del archivo de la imagen.

    Returns:
        Response: La imagen mostrar desde el directorio o un error si no se encuentra.
    """
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        print(f"Error al mostrar la imagen: {e}")
        raise FileNotFoundError(f"No se pudo mostrar la imagen: {e}")
    
def verify_camera_key(key):
    """
    Verifica si la clave proporcionada es válida.
    Args:
        key (str): Clave enviada desde el Arduino.
    Returns:
        bool: True si la clave es válida, False en caso contrario.
    """
    return key == CAMERA_SECRET_KEY

def get_paginated_photos(page, limit):
    rows = get_photos_paginated(page, limit)
    
    images = [
        {
            'filename': row[0],
            'url': f"http://{IP}:{PORT}/photos/uploads/{row[0]}",
            'timestamp': row[2].strftime("%Y-%m-%d %H:%M:%S"),
            'personDetected': row[3]
        }
        for row in rows
    ]
    return images