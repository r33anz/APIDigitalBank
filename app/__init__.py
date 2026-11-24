from flask import Flask
from .config import config_map
from .extensions import db, jwt, bcrypt, migrate

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Registrar controladores (blueprints) <--- AQUÍ VA
    from .controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Importar modelos para que Flask-Migrate los detecte
    from . import models  # noqa

    return app