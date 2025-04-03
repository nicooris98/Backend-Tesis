from .auth_routes import auth_bp
from .photos_routes import photos_bp

def register_blueprints(app):
    #app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(photos_bp, url_prefix='/photos')
