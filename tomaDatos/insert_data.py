from app import create_app, db
from app.models import TipoParo, Producto, Usuario

def insertar_tipos_paro():
    app = create_app()
    with app.app_context():
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
        print("✅ Tipos de paro insertados correctamente.")

def insertar_productos():
    app = create_app()
    with app.app_context():
        productos = [
            {"referencia": "P03-94", "nombre": "Platano"},
            {"referencia": "P01-94", "nombre": "Platano"},
            {"referencia": "P05-94", "nombre": "Platano"},
            {"referencia": "P07-94", "nombre": "Platano"},
            {"referencia": "P09-94", "nombre": "Platano"},
            {"referencia": "P11-94", "nombre": "Platano"},
            {"referencia": "P04-94", "nombre": "Platano"},
            {"referencia": "P02-94", "nombre": "Platano"},
            {"referencia": "P06-94", "nombre": "Platano"},
            {"referencia": "P08-94", "nombre": "Platano"},
            {"referencia": "P10-94", "nombre": "Platano"},
            {"referencia": "P12-94", "nombre": "Platano"},
            {"referencia": "B32", "nombre": "Banano"},
            {"referencia": "BC32", "nombre": "Banano"},
            {"referencia": "B36", "nombre": "Banano"},
            {"referencia": "B34", "nombre": "Banano"},
            {"referencia": "BC34-160", "nombre": "Banano"},
            {"referencia": "BC34-165", "nombre": "Banano"},
            {"referencia": "B40", "nombre": "Banano"},
            {"referencia": "B42", "nombre": "Banano"},
            {"referencia": "B44", "nombre": "Banano"},
            {"referencia": "B31", "nombre": "Banano"},
            {"referencia": "B35", "nombre": "Banano"},
            {"referencia": "B35-35", "nombre": "Banano"},
            {"referencia": "B35-32", "nombre": "Banano"},
            {"referencia": "B35-40", "nombre": "Banano"},
            {"referencia": "B33", "nombre": "Banano"},
            {"referencia": "B41", "nombre": "Banano"},
            {"referencia": "B45", "nombre": "Banano"},
            {"referencia": "B43", "nombre": "Banano"}
        ]

        for producto in productos:
            if not Producto.query.filter_by(referencia=producto["referencia"]).first():
                nuevo_producto = Producto(
                    referencia=producto["referencia"],
                    nombre=producto["nombre"]
                )
                db.session.add(nuevo_producto)

        db.session.commit()
        print("✅ Productos insertados correctamente.")

def insertar_usuarios():
    app = create_app()
    with app.app_context():
        usuarios = [
            {"usuario": f"operario_{str(i+1).zfill(2)}", "nombre": nombre, "password": password}
            for i, (nombre, password) in enumerate([
                ("Julian Andres Orozco", "9790733"),
                ("Noe Muñoz Valencia", "18370919"),
                ("Jose Yovanny Arango lopez", "9790807"),
                ("Norbey Estiben Grisales Domínguez", "1093799409"),
                ("Andres Giraldo Londoño", "1088324589"),
                ("Jose Norbey Gomez Barbosa", "1097726570"),
                ("Nestor Daniel Molina Marín", "1094882086"),
                ("Jhorman Andrés Iza Marin", "1094976425"),
                ("Manuel Ernesto López", "80369635"),
                ("Luis Norbey López Sanchez", "9729879"),
                ("Claudia Maria Aldana", "41926055"),
                ("Cristhian Joany Rios De Los Rios", "75102969"),
                ("Gildardo Cruz", "18397709"),
                ("Diego Alejandro Vallejo Correa", "1098313612"),
                ("Andres Juan Alzate Ospina", "1004799080"),
                ("Ivan Andres Arias Ladino", "1096040398")
            ])
        ]

        for usuario in usuarios:
            if not Usuario.query.filter_by(usuario=usuario["usuario"]).first():
                nuevo_usuario = Usuario(
                    usuario=usuario["usuario"],
                    nombre=usuario["nombre"]
                )
                nuevo_usuario.set_password(usuario["password"])
                db.session.add(nuevo_usuario)

        db.session.commit()
        print("✅ Usuarios insertados correctamente.")

if __name__ == "__main__":
    insertar_tipos_paro()
    insertar_productos()
    insertar_usuarios()