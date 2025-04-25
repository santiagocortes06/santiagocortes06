from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    # Configuración de la aplicación Flask
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configurar upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Registrar blueprints
    from app.routes import main_bd
    from app.errors import bp as errors_bp
    app.register_blueprint(main_bd)
    app.register_blueprint(errors_bp)
    
    # Crear tablas de base de datos
   # with app.app_context():
      #  db.create_all()
    
    return app

# Importar modelos al final para evitar importaciones circulares
from app.models import Usuario