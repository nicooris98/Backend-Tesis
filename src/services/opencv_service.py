import cv2
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()

# Cargar modelo preentrenado de MobileNet SSD
prototxt_path = os.getenv('PROTOTXT_PATH')
model_path = os.getenv('MODEL_PATH')
print(prototxt_path, model_path)
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

def detect_person(image_path):
    """
    Detecta si hay una persona en una imagen utilizando MobileNet SSD.
    
    Args:
        image_path (str): Ruta al archivo de imagen.
    
    Returns:
        bool: True si se detectó una persona, False en caso contrario.
    """
    try:
        # Leer la imagen
        image = cv2.imread(image_path)
        (h, w) = image.shape[:2]

        # Preprocesar la imagen para pasarla al modelo
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # Analizar las detecciones
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:  # Filtrar por nivel de confianza
                idx = int(detections[0, 0, i, 1])
                if idx == 15:  # El índice 15 corresponde a "persona" en MobileNet SSD
                    return True
        return False
    except Exception as e:
        print(f"Error en la detección: {e}")
        return False
