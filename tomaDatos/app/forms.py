from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DecimalField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(max=100)])
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class FinalizarTurnoForm(FlaskForm):
    # Campos de producción
    kg_conformes = DecimalField('Kg Conformes', places=2, validators=[
        DataRequired(),
        NumberRange(min=0, message="No puede ser negativo")
    ])
    rollos = IntegerField('Cantidad de Rollos', validators=[
        DataRequired(),
        NumberRange(min=1, message="Debe ser positivo")
    ])
    capas = IntegerField('Capas', validators=[
        Optional(),
        NumberRange(min=1, message="Debe ser positivo")
    ])
    
    # Campos de desperdicio
    merma = DecimalField('Merma (kg)', places=2, validators=[
        DataRequired(), 
        NumberRange(min=0, message="No puede ser negativo")
    ])
    retal = DecimalField('Retal (kg)', places=2, validators=[
        DataRequired(), 
        NumberRange(min=0, message="No puede ser negativo")
    ])
    
    # Observaciones
    descripcion = TextAreaField('Observaciones', validators=[
        Optional(),
        Length(max=500)
    ])
    
    submit = SubmitField('Finalizar Turno')

class RegistrarCapasForm(FlaskForm):
    capas = IntegerField('Capas', validators=[
        DataRequired(),
        NumberRange(min=0, message="No puede ser negativo")
    ])
    submit = SubmitField('Registrar Capas')