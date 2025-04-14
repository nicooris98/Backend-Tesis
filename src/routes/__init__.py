from .auth_routes import auth_bp
from .photos_routes import photos_blueprint

def register_blueprints(app, socketio):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(photos_blueprint(socketio), url_prefix='/photos')
