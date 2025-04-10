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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def insert_user(username, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash) 
            VALUES (%s, %s)
        ''', (username, password_hash))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error al registrar usuario: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, password_hash
        FROM users
        WHERE username = %s
    ''', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_photos_paginated(page, per_page):
    """
    Recupera las fotos de forma paginada.
    
    Args:
        page (int): Número de la página solicitada.
        per_page (int): Número de elementos por página.
    
    Returns:
        list: Fotos de la base de datos en el rango paginado.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calcular el OFFSET (inicio de los resultados)
    offset = (page - 1) * per_page

    # Consulta con paginación
    cursor.execute('''
        SELECT filename, filepath, timestamp, person_detected
        FROM photos
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
    ''', (per_page, offset))
    
    photos = cursor.fetchall()
    cursor.close()
    conn.close()

    return photos
