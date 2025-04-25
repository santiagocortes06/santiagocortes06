from app import create_app, db
from app.models import TipoParo

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

if __name__ == "__main__":
    insertar_tipos_paro()