from flask import Blueprint, render_template  # Importar Blueprint aquí
from app import db  # Importar db desde el módulo app

def page_not_found(e):
    return render_template('errors/404.html'), 404

def internal_server_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500

def forbidden(e):
    return render_template('errors/403.html'), 403

# Crear blueprint de errores
bp = Blueprint('errors', __name__)