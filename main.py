from flask import Flask, request
import os
import time
import cv2
import numpy as np

app = Flask(__name__)

# Carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar el modelo preentrenado de MobileNet SSD
prototxt_path = 'deploy.prototxt'
model_path = 'mobilenet_iter_73000.caffemodel'
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        timestamp = int(time.time())
        filename = f"{timestamp}_{file.filename}"
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
        if person_detected:
            print('Persona detectada en la imagen')
        else:
            print('No se detectó ninguna persona en la imagen')
        return 'File successfully uploaded', 200

if __name__ == '__main__':
    app.run(port=3000)
