import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')

# Función para inicializar la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    return conn

# Función para inicializar la tabla (solo se ejecuta una vez al inicio)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            person_detected BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Función para insertar registros
def insert_photo(filename, filepath, timestamp, person_detected):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO photos (filename, filepath, timestamp, person_detected)
        VALUES (%s, %s, %s, %s)
    ''', (filename, filepath, timestamp, person_detected))
    conn.commit()
    cursor.close()
    conn.close()

# Función para obtener las últimas imágenes
def get_latest_photos(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT filename, filepath, timestamp, person_detected
        FROM photos
        ORDER BY timestamp DESC
        LIMIT %s
    ''', (limit,))
    photos = cursor.fetchall()
    cursor.close()
    conn.close()
    return photos
