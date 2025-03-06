# Backend Flask - Tesis
Este backend esta hecho con flask y opencv.

# Instalacion de programas
Hay que instalar python y pip y postgres.

# Instalacion de dependencias
Hay que instalar las siguientes dependencias.
```bash
pip install opencv-python numpy flask imutils python-dotenv psycopg2-binary flask-cors
```

# Variables de entorno
Si se necesita modificar algo de los archivos o modelos o puerto debe hacerlo en el archivo `.env`.

# Correr el proyecto
Para correr el proyecto usa el archivo `main.py`.
```bash
python main.py
```

# Prueba con postman
Se puede probar con postman, para ello hay que crear un POST a `http://127.0.0.1:3000/upload`.
En el tab de headers hay que agregar en key: `Content-type` y en value: `multipart/form-data`.
En el tab body hay que apretar el check que dice `form-data`, en la key: `file` de tipo `File` en el dropdown y en value seleccionar una imagen.
Luego le da a Send para probar y deberia recibir `File successfully uploaded` con codigo `200` si todo salio bien.
Si quiere saber si se detecto o no una persona tiene que fijarse en la terminal donde este corriendo el codigo.

# Error en la instalacion
Si da error con algun paquete entonces instalalo.
```bash
pip install <nombre_del_paquete_faltante>
```