from app import create_app, db
from app.models import Usuario, Maquina, Producto, Turno, TipoParo
from werkzeug.security import generate_password_hash
from datetime import time

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existen usuarios para no duplicar
        if not Usuario.query.first():
            # ===== 1. CREACIÓN DE USUARIOS =====
            admin = Usuario(
                usuario="admin",
                nombre="Administrador Principal",
                activo=True
            )
            admin.set_password('Admin123*')
            
            operario_principal = Usuario(
                usuario="oper_principal",
                nombre="Operario Principal",
                activo=True
            )
            operario_principal.set_password('Operario123*')
            
            operario_ayudante = Usuario(
                usuario="oper_ayudante",
                nombre="Operario Ayudante",
                activo=True
            )
            operario_ayudante.set_password('Ayudante123*')
            
            db.session.add_all([admin, operario_principal, operario_ayudante])
            
            # ===== 2. CREACIÓN DE MÁQUINAS =====
            maquinas = [
                Maquina(nombre="Extrusora 1"),
                Maquina(nombre="Extrusora 2"),
                Maquina(nombre="Extrusora 3"),
                Maquina(nombre="Extrusora 4"),
                Maquina(nombre="Perforadora 1"),
                Maquina(nombre="Perforadora 2")
            ]
            db.session.add_all(maquinas)
            
            # ===== 3. CREACIÓN DE PRODUCTOS =====
            productos = [
                Producto(referencia="P01", nombre="Producto 01"),
                Producto(referencia="P03", nombre="Producto 03")
            ]
            db.session.add_all(productos)
            
            # ===== 4. CREACIÓN DE TURNOS =====
            turnos = [
                Turno(nombre="Día", duracion_horas=8),
                Turno(nombre="Tarde", duracion_horas=8),
                Turno(nombre="Noche", duracion_horas=8),
                Turno(nombre="Día 12h", duracion_horas=12),
                Turno(nombre="Noche 12h", duracion_horas=12)
            ]
            db.session.add_all(turnos)
            
            # ===== 5. CREACIÓN DE TIPOS DE PARO =====
            tipos_paro = [
                "alistamiento",
                "programado",
                "calidad",
                "averias",
                "organizacional"
            ]

            for tipo in tipos_paro:
                if not TipoParo.query.filter_by(nombre=tipo).first():
                    nuevo_tipo = TipoParo(nombre=tipo)
                    db.session.add(nuevo_tipo)
            
            db.session.commit()
            
            print("✅ Datos maestros creados exitosamente:")
            print(f"- 3 usuarios (admin, operario principal, operario ayudante)")
            print(f"- 6 máquinas (4 extrusoras, 2 perforadoras)")
            print(f"- 2 productos (P01, P03)")
            print(f"- 5 turnos (8h y 12h)")
            print(f"- 5 tipos de paro (alistamiento, programado, calidad, averias, organizacional)")
            print("\nℹ️ No se crearon registros de producción ni paradas iniciales")
        else:
            print("ℹ️ La base de datos ya contiene datos (no se ejecutó seeding)")

if __name__ == '__main__':
    seed_database()