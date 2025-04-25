from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

# Inicializar extensiones (sin dependencias de app)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Factory principal para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuración adicional
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB límite upload

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configuración de login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
    login_manager.login_message_category = 'warning'

    # Registrar blueprints (rutas)
    from app.routes import main_bd
    from app.errors import bp as errors_bp
    app.register_blueprint(main_bd)
    app.register_blueprint(errors_bp)

    # Registrar comandos CLI
    from app.commands import register_commands
    register_commands(app)

    # Configurar user_loader dentro del contexto de la aplicación
    with app.app_context():
        from app.models import Usuario
        
        @login_manager.user_loader
        def load_user(user_id):
            return Usuario.query.get(int(user_id))
        
        # Crear tablas solo en desarrollo
        if app.config['FLASK_ENV'] == 'development':
            db.create_all()

    # Configurar handlers de error
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    """Registra manejadores de errores personalizados"""
    from app.errors import page_not_found, internal_server_error, forbidden
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(403, forbidden)