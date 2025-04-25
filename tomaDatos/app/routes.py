from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
from app.forms import LoginForm, RegistroForm, FinalizarTurnoForm
from app.models import (
    Usuario, 
    Parada, 
    RegistroProduccion, 
    Maquina, 
    Turno, 
    Producto,
    TipoParo
)
from app import db, login_manager
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configurar el registro de mensajes
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Crear un blueprint para las rutas principales
main_bd = Blueprint('main', __name__)

@main_bd.app_context_processor
def inject_now():
    return {'now': datetime.now()}

# --- Helpers ---
def calcular_duracion(inicio, fin=None):
    fin = fin or datetime.now()
    diferencia = fin - inicio
    horas, remainder = divmod(diferencia.total_seconds(), 3600)
    minutos, _ = divmod(remainder, 60)
    return f"{int(horas)}h {int(minutos)}m"

# --- Rutas Principales ---
@main_bd.route('/')
@login_required
def index():
    return render_template('seleccion_modulo.html')

@main_bd.route('/produccion')
@login_required
def registros_activos():
    """Muestra la tabla de registros de producción activos"""
    try:
        producciones = RegistroProduccion.query.filter(
            RegistroProduccion.hora_fin.is_(None),  # Solo registros no finalizados
            RegistroProduccion.id_usuario_principal == current_user.id
        ).all()
        return render_template('registros_activos.html', producciones=producciones)
    except Exception as e:
        flash('Error al cargar los registros de producción', 'danger')
        return render_template('registros_activos.html', producciones=[])

@main_bd.route('/iniciar-produccion')
@login_required
def iniciar_produccion():
    try:
        maquinas = Maquina.query.all()
        turnos = Turno.query.all()
        productos = Producto.query.all()
        return render_template('produccion/iniciar_turno.html', 
                            maquinas=maquinas, 
                            turnos=turnos, 
                            productos=productos)
    except Exception as e:
        flash('Error al cargar los datos de producción', 'danger')
        return redirect(url_for('main.index'))

@main_bd.route('/detalles-produccion/<int:id_registro>', methods=['GET', 'POST'])
@login_required
def detalles_produccion(id_registro):
    """Renderiza la página de detalles de producción para un registro específico."""
    registro = RegistroProduccion.query.get_or_404(id_registro)
    productos = Producto.query.all()  # Obtener lista de productos
    return render_template('produccion/detalles_produccion.html', 
                         registro=registro,
                         productos=productos)

@main_bd.route('/detalles-produccion-multiple/<registro_ids>')
@login_required
def detalles_produccion_multiple(registro_ids):
    """Renderiza la página de detalles de producción para múltiples registros."""
    try:
        # Convertir la cadena de IDs en una lista
        ids = [int(id) for id in registro_ids.split(',')]
        
        # Obtener todos los registros
        registros = RegistroProduccion.query.filter(
            RegistroProduccion.id.in_(ids),
            RegistroProduccion.hora_fin.is_(None)  # Solo registros activos
        ).all()
        
        # Obtener productos para los selectores
        productos = Producto.query.all()
        
        return render_template('produccion/detalles_produccion_multiple.html',
                           registros=registros,
                           productos=productos)
    except Exception as e:
        flash('Error al cargar los detalles de producción', 'danger')
        return redirect(url_for('main.registros_activos'))

@main_bd.route('/iniciar_turno', methods=['POST'])
@login_required
def iniciar_turno():
    try:
        # Obtener datos del formulario
        id_turno = request.form.get('turno')
        id_ayudante = request.form.get('ayudante')
        maquinas_ids = request.form.getlist('maquinas[]')

        if not maquinas_ids or not id_turno:
            flash('Debe seleccionar al menos una máquina y un turno', 'danger')
            return redirect(url_for('main.iniciar_produccion'))

        registros_creados = []
        for id_maquina in maquinas_ids:
            nuevo_registro = RegistroProduccion(
                id_maquina=id_maquina,
                id_usuario_principal=current_user.id,
                id_usuario_ayudante=id_ayudante if id_ayudante else None,
                id_turno=id_turno,
                hora_inicio=datetime.now().time()
            )
            db.session.add(nuevo_registro)
            registros_creados.append(nuevo_registro)

        db.session.commit()
        
        # Redirigir a la vista múltiple con los IDs de los registros
        registro_ids = ','.join(str(r.id) for r in registros_creados)
        return redirect(url_for('main.detalles_produccion_multiple', registro_ids=registro_ids))

    except Exception as e:
        db.session.rollback()
        print(f"Error al iniciar turno: {str(e)}")
        flash('Error al iniciar el turno', 'danger')
        return redirect(url_for('main.iniciar_produccion'))

@main_bd.route('/asignar_producto/<int:id_registro>', methods=['POST'])
@login_required
def asignar_producto(id_registro):
    try:
        registro = RegistroProduccion.query.get_or_404(id_registro)
        producto_id = request.form.get('producto')

        if not producto_id:
            flash('Debe seleccionar un producto', 'danger')
            return redirect(request.referrer)

        registro.id_producto = producto_id
        db.session.commit()
        flash('Producto asignado correctamente', 'success')
        return redirect(url_for('main.detalles_produccion', id_registro=id_registro))

    except Exception as e:
        db.session.rollback()
        flash('Error al asignar el producto', 'danger')
        return redirect(request.referrer)

@main_bd.route('/finalizar_turno/<int:id_registro>', methods=['GET', 'POST'])
@login_required
def finalizar_turno(id_registro):
    registro = RegistroProduccion.query.get_or_404(id_registro)

    if request.method == 'POST':
        try:
            # Guardar la hora de finalización del turno
            registro.hora_fin = datetime.now().time()
            db.session.commit()
            flash('Turno finalizado correctamente', 'success')
            return redirect(url_for('main.finalizar_turno', id_registro=id_registro))
        except Exception as e:
            db.session.rollback()
            flash('Error al finalizar el turno', 'danger')
            return redirect(url_for('main.registros_activos'))

    # Calcular duración del turno
    if registro.hora_inicio and registro.hora_fin:
        inicio_datetime = datetime.combine(registro.fecha, registro.hora_inicio)
        fin_datetime = datetime.combine(registro.fecha, registro.hora_fin)
        if fin_datetime < inicio_datetime:
            fin_datetime += timedelta(days=1)
        duracion_turno = fin_datetime - inicio_datetime
        horas_trabajadas = duracion_turno.total_seconds() / 3600
    else:
        horas_trabajadas = 0

    # Calcular tiempo de paro
    tiempo_paro = sum(parada.duracion_minutos for parada in registro.paradas) / 60  # Convertir a horas

    return render_template('produccion/finalizar_turno.html', 
                           registro=registro,
                           horas_trabajadas=horas_trabajadas,
                           tiempo_paro=tiempo_paro)

# --- Gestión de Paradas ---
@main_bd.route('/registrar_paro/<int:id_registro>', methods=['GET', 'POST'])
@login_required
def registrar_paro(id_registro):
    try:
        registro = RegistroProduccion.query.get_or_404(id_registro)
        
        if request.method == 'GET':
            # Redirigir a la vista anterior
            return redirect(request.referrer or url_for('main.detalles_produccion_multiple', registro_ids=id_registro))
            
        # Crear nuevo paro
        nueva_parada = Parada(
            registro_id=id_registro,
            inicio=datetime.now()
        )
        db.session.add(nueva_parada)
        db.session.commit()
        flash('Paro iniciado correctamente', 'success')
        return redirect(request.referrer)
        
    except Exception as e:
        db.session.rollback()
        flash('Error al iniciar el paro', 'danger')
        return redirect(request.referrer)

@main_bd.route('/finalizar_paro/<int:id_registro>', methods=['GET', 'POST'])
@login_required
def finalizar_paro(id_registro):
    registro = RegistroProduccion.query.get_or_404(id_registro)
    parada = Parada.query.filter_by(registro_id=id_registro, fin=None).first()

    if not parada:
        flash('No hay un paro activo para finalizar', 'danger')
        return redirect(request.referrer)

    if request.method == 'POST' and 'tipo_paro' in request.form:
        parada.fin = datetime.now()
        parada.duracion_minutos = parada.calcular_duracion()
        tipo_paro_id = request.form.get('tipo_paro', type=int)
        parada.tipo_paro_id = tipo_paro_id

        # Actualizar la suma de minutos por tipo de paro en la tabla registro_produccion
        if tipo_paro_id:
            tipo_paro = TipoParo.query.get(tipo_paro_id)
            if tipo_paro.nombre == 'alistamiento':
                registro.suma_minutos_alistamiento += parada.duracion_minutos
            elif tipo_paro.nombre == 'programado':
                registro.suma_minutos_programado += parada.duracion_minutos
            elif tipo_paro.nombre == 'calidad':
                registro.suma_minutos_calidad += parada.duracion_minutos
            elif tipo_paro.nombre == 'averias':
                registro.suma_minutos_averias += parada.duracion_minutos
            elif tipo_paro.nombre == 'organizacional':
                registro.suma_minutos_organizacional += parada.duracion_minutos

        # Guardar la hora de finalización en la tabla registro_produccion
        registro.hora_fin = datetime.now().time()

        db.session.commit()
        flash('Paro finalizado correctamente', 'success')
        return redirect(url_for('main.detalles_produccion', id_registro=id_registro))

    tipos_paro = TipoParo.query.all()
    return render_template('produccion/finalizar_paro.html', 
                         registro=registro, 
                         parada=parada, 
                         tipos_paro=tipos_paro)

@main_bd.route('/registrar_peso_rollo/<int:id_registro>', methods=['POST'])
@login_required
def registrar_peso_rollo(id_registro):
    registro = RegistroProduccion.query.get_or_404(id_registro)
    peso = request.form.get('peso', type=float)
    if peso:
        registro.kg_conformes += peso
        registro.rollos += 1
        db.session.commit()
        flash('Peso del rollo registrado correctamente', 'success')
    else:
        flash('Error al registrar el peso del rollo', 'danger')
    return redirect(request.referrer)

@main_bd.route('/registrar_retal/<int:id_registro>', methods=['POST'])
@login_required
def registrar_retal(id_registro):
    registro = RegistroProduccion.query.get_or_404(id_registro)

    if registro.retal > 0:
        flash('El retal ya ha sido registrado para este turno.', 'danger')
        return redirect(request.referrer)

    retal = request.form.get('retal', type=float)
    if retal:
        registro.retal += retal
        db.session.commit()
        flash('Retal registrado correctamente', 'success')
    else:
        flash('Error al registrar el retal', 'danger')
    return redirect(request.referrer)

@main_bd.route('/registrar_aleluya/<int:id_registro>', methods=['POST'])
@login_required
def registrar_aleluya(id_registro):
    registro = RegistroProduccion.query.get_or_404(id_registro)

    if registro.merma > 0:
        flash('La merma ya ha sido registrada para este turno.', 'danger')
        return redirect(request.referrer)

    aleluya = request.form.get('aleluya', type=float)
    if aleluya:
        registro.merma += aleluya
        db.session.commit()
        flash('Aleluya registrada correctamente', 'success')
    else:
        flash('Error al registrar la aleluya', 'danger')
    return redirect(request.referrer)

@main_bd.route('/registrar_capas/<int:id_registro>', methods=['POST'])
@login_required
def registrar_capas(id_registro):
    registro = RegistroProduccion.query.get_or_404(id_registro)

    if registro.capas is not None and registro.capas > 0:
        flash('Las capas ya han sido registradas para este turno.', 'danger')
        return redirect(request.referrer)

    capas = request.form.get('capas', type=int)
    if capas:
        registro.capas = capas
        db.session.commit()
        flash('Capas registradas correctamente', 'success')
    else:
        flash('Error al registrar las capas', 'danger')
    return redirect(request.referrer)

# --- Autenticación ---
@main_bd.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Usuario.query.filter_by(usuario=form.usuario.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('main.index'))
            flash('Usuario o contraseña incorrectos', 'danger')
        except Exception as e:
            flash('Error al iniciar sesión', 'danger')

    return render_template('auth/login.html', form=form)

@main_bd.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bd.route('/registro', methods=['GET', 'POST'])
@login_required
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        try:
            user = Usuario(
                nombre=form.nombre.data,
                usuario=form.usuario.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar usuario: {str(e)}', 'danger')

    return render_template('registro.html', form=form)