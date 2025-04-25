from datetime import datetime, time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model, UserMixin):
    """Modelo simplificado de usuarios"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    registros_principal = db.relationship('RegistroProduccion', 
                                       foreign_keys='RegistroProduccion.id_usuario_principal',
                                       backref='operario_principal')
    registros_ayudante = db.relationship('RegistroProduccion',
                                       foreign_keys='RegistroProduccion.id_usuario_ayudante',
                                       backref='operario_ayudante')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

class Maquina(db.Model):
    """Modelo simplificado de máquinas"""
    __tablename__ = 'maquinas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Relación con registros de producción
    producciones = db.relationship('RegistroProduccion', backref='maquina')

class Producto(db.Model):
    """Modelo simplificado de productos"""
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    referencia = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Relación
    producciones = db.relationship('RegistroProduccion', backref='producto')

class Turno(db.Model):
    """Modelo simplificado de turnos"""
    __tablename__ = 'turnos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    duracion_horas = db.Column(db.Integer, nullable=False)
    
    # Relación
    producciones = db.relationship('RegistroProduccion', backref='turno')

class RegistroProduccion(db.Model):
    """Modelo principal de registro de producción"""
    __tablename__ = 'registro_produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    
    # Relaciones
    id_maquina = db.Column(db.Integer, db.ForeignKey('maquinas.id'), nullable=False)
    id_usuario_principal = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_usuario_ayudante = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'))
    id_turno = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
    
    # Horarios
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    
    # Producción
    kg_conformes = db.Column(db.Float, default=0.0)
    rollos = db.Column(db.Integer, default=0)
    retal = db.Column(db.Float, default=0.0)
    merma = db.Column(db.Float, default=0.0)
    capas = db.Column(db.Integer, default=0)
    
    # Paros resumidos
    suma_minutos_alistamiento = db.Column(db.Integer, default=0)
    suma_minutos_programado = db.Column(db.Integer, default=0)
    suma_minutos_calidad = db.Column(db.Integer, default=0)
    suma_minutos_averias = db.Column(db.Integer, default=0)
    suma_minutos_organizacional = db.Column(db.Integer, default=0)
    
    descripcion = db.Column(db.Text)
    
    # Relación con paradas (usando backref desde Parada)

class Parada(db.Model):
    """Modelo actualizado de paros"""
    __tablename__ = 'paradas'

    id = db.Column(db.Integer, primary_key=True)
    tipo_paro_id = db.Column(db.Integer, db.ForeignKey('tipos_paros.id'), nullable=True)
    registro_id = db.Column(db.Integer, db.ForeignKey('registro_produccion.id'), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fin = db.Column(db.DateTime)
    duracion_minutos = db.Column(db.Integer)

    # Relaciones
    tipo_paro = db.relationship('TipoParo', backref='paradas')
    registro = db.relationship('RegistroProduccion', backref='paradas')

    def calcular_duracion(self):
        if self.inicio and self.fin:
            diff = self.fin - self.inicio
            self.duracion_minutos = int(diff.total_seconds() / 60)
        return self.duracion_minutos

class TipoParo(db.Model):
    """Modelo para los tipos de paros"""
    __tablename__ = 'tipos_paros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<TipoParo {self.nombre}>'