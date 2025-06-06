# Backend Flask - Tesis
Este backend esta hecho con flask y opencv.

# Instalacion de programas
Hay que instalar python y pip y postgres.

# Entorno virtual
Un entorno virtual es un espacio aislado donde puedes instalar paquetes de Python sin afectar el resto de tu sistema o tus otros proyectos.

## Creacion del entorno
```bash
py -3 -m venv .venv
```

## Activar el entorno
Antes de trabajar en su proyecto, active el entorno correspondiente:

```bash
.venv\Scripts\activate
```

El prompt del shell cambiará para mostrar el nombre del entorno activado.

## Desactivar el entorno
En un entorno activado, ejecutar:

```bash
deactivate
```

# Instalacion de dependencias
Hay que instalar las siguientes dependencias.
```bash
pip install opencv-python numpy flask imutils python-dotenv psycopg2-binary flask-cors PyJWT flask-socketio eventlet
```

## Instalar con archivo requirements.txt
```bash
pip install -r requirements.txt
```

# Variables de entorno
Si se necesita modificar algo de los archivos o modelos o puerto debe hacerlo en el archivo `.env`.

# Correr el proyecto
Para correr el proyecto usa el archivo `main.py`.
```bash
python main.py
```

# Prueba de Endpoints
Se recomienda usar postman.
## Registro de usuario, login y token
Para poder registrarse hay que ir al endpoint `http://127.0.0.1:3000/auth/register` y realizar una peticion POST y con el siguiente body:
```json
{
    "username": "testuser",
    "password": "123456"
}
```
Luego para el login el endpoint es `http://127.0.0.1:3000/auth/login` y en el body poner un usuario registrado:
```json
{
    "username": "testuser",
    "password": "123456"
}
```
Esto devolvera un token el cual pegaremos en todas las peticiones que realicemos y para ello hay que ir al tab de Authorization, seleccionar Bearer Token y pegar el token que da el login.
## Subida de archivos
Hay que crear una peticion POST a `http://127.0.0.1:3000/photos/upload`.
En el tab de headers hay que agregar en key: `Content-type` y en value: `multipart/form-data`.
En el tab body hay que apretar el check que dice `form-data`, en la key: `file` de tipo `File` en el dropdown y en value seleccionar una imagen.
El otro header que hay que agregar es `Camera-Key` y el valor que este en la variable de entorno.
Luego le da a Send para probar y deberia recibir `File successfully uploaded` con codigo `200` si todo salio bien.
Si quiere saber si se detecto o no una persona tiene que fijarse en la terminal donde este corriendo el codigo.

# Error en la instalacion
Si da error con algun paquete entonces instalalo.
```bash
pip install <nombre_del_paquete_faltante>
```
# Archivo .env
Existe el archivo `.env.development` el cual se debe usar como plantilla para el archivo `.env` que debe crear en el proyecto.