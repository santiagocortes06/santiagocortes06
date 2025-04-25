import click
from werkzeug.security import generate_password_hash
from flask import current_app
from app import db

def register_commands(app):
    @app.cli.command('seed-users')
    def seed_users():
        """Carga usuarios iniciales en la BD"""
        from app.models import Usuario  # Importación local para evitar problemas
        
        users_data = [
            {
                'nombre': 'Admin Principal',
                'usuario': 'admin',
                'password': 'Admin123*',  # En producción usa variables de entorno
                'cedula': '123456789',
                'correo': 'admin@agrobol.com',
                'rol': 'administrador',
                'estado': True
            },
            {
                'nombre': 'Supervisor 1',
                'usuario': 'supervisor1',
                'password': 'Super123*',
                'cedula': '987654321',
                'correo': 'supervisor@agrobol.com',
                'rol': 'supervisor',
                'estado': True
            },
            {
                'nombre': 'Operario 1',
                'usuario': 'operario1',
                'password': 'Oper123*',
                'cedula': '111222333',
                'correo': 'operario@agrobol.com',
                'rol': 'operario',
                'estado': True
            }
        ]

        try:
            with current_app.app_context():  # Aseguramos el contexto
                for user_data in users_data:
                    if not Usuario.query.filter_by(usuario=user_data['usuario']).first():
                        user = Usuario(
                            nombre=user_data['nombre'],
                            usuario=user_data['usuario'],
                            cedula=user_data['cedula'],
                            correo=user_data['correo'],
                            rol=user_data['rol'],
                            estado=user_data['estado']
                        )
                        user.set_password(user_data['password'])  # Usamos el método del modelo
                        db.session.add(user)
                        click.echo(f"↑ Usuario {user_data['usuario']} creado")
                    else:
                        click.echo(f"→ Usuario {user_data['usuario']} ya existe")
                
                db.session.commit()
                click.echo("✅ Usuarios cargados exitosamente!")
        except Exception as e:
            db.session.rollback()
            click.echo(f"❌ Error: {str(e)}", err=True)

    @app.cli.command('list-users')
    def list_users():
        """Lista todos los usuarios en la BD"""
        from app.models import Usuario
        
        try:
            with current_app.app_context():
                users = Usuario.query.all()
                if not users:
                    click.echo("No hay usuarios registrados")
                    return
                
                click.echo("\nUSUARIOS REGISTRADOS:")
                click.echo("-" * 50)
                for user in users:
                    click.echo(f"ID: {user.id} | Usuario: {user.usuario}")
                    click.echo(f"Nombre: {user.nombre} | Rol: {user.rol}")
                    click.echo(f"Email: {user.correo} | Activo: {'Sí' if user.estado else 'No'}")
                    click.echo("-" * 50)
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}", err=True)