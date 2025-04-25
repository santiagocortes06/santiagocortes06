import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class Config:
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    
    # Configuración de base de datos con parámetros codificados
    DB_PARAMS: Dict[str, Any] = {
        'username': os.environ.get('DB_USER', 'flask_user'),
        'password': quote_plus(os.environ.get('DB_PASSWORD', 'FlaskDB')),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME', 'agrobol_db')
    }
    
    # URI de conexión mejorada
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_PARAMS['username']}:{DB_PARAMS['password']}"
        f"@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}"
        "?client_encoding=utf8"
        "&connect_timeout=10"  # Timeout de conexión
        "&keepalives=1"  # Mantener conexión activa
        "&keepalives_idle=30"  # Tiempo idle para keepalive
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verificar conexión antes de usarla
        'pool_recycle': 3600,  # Reciclar conexiones cada 1 hora
        'pool_size': 10,  # Tamaño máximo del pool
        'max_overflow': 5  # Conexiones adicionales permitidas
    }
    
    # Configuración de seguridad adicional
    SESSION_COOKIE_SECURE = FLASK_ENV == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de archivos subidos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB límite de upload

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Mostrar queries SQL en consola
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'