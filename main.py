from flask import Flask, request
import os
import cv2
import numpy as np
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar el modelo preentrenado de MobileNet SSD
prototxt_path = os.getenv('PROTOTXT_PATH')
model_path = os.getenv('MODEL_PATH')
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

port = int(os.getenv('PORT', 3000))

database_url = os.getenv('DATABASE_URL')

# Conectar a la base de datos PostgreSQL
conn = psycopg2.connect(database_url)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS photos
             (id SERIAL PRIMARY KEY,
              filename TEXT NOT NULL,
              filepath TEXT NOT NULL,
              timestamp TIMESTAMP NOT NULL,
              person_detected BOOLEAN NOT NULL)''')
conn.commit()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y%m%d%H%M%S")
        extension = os.path.splitext(file.filename)[1]
        filename = f"{date_str}{extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Analizar la imagen para detectar personas
        image = cv2.imread(filepath)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        person_detected = False
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                if idx == 15:  # El índice 15 corresponde a personas en MobileNet SSD
                    person_detected = True
                    break

        # Insertar datos en la base de datos PostgreSQL
        c.execute("INSERT INTO photos (filename, filepath, timestamp, person_detected) VALUES (%s, %s, %s, %s)",
                  (filename, filepath, timestamp, person_detected))
        conn.commit()
        
        if person_detected:
            print('Persona detectada en la imagen')
        else:
            print('No se detectó ninguna persona en la imagen')
        return 'File successfully uploaded', 200

if __name__ == '__main__':
    app.run(port=port)
