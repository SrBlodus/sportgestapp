from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from config import Config

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar la configuración desde config.py
    app.config.from_object(Config)

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Registrar el blueprint
    from app.routes.persona_routes import persona_bp
    app.register_blueprint(persona_bp, url_prefix='/personas')

    with app.app_context():
        # Importar tus modelos aquí
        from app.models import Persona, Sexo, Nacionalidad, EstadoCivil, User, Tutor, TipoPersona, TipoDocumento, Role, PersonaXTipoDoc, PersonaXTipo

        # Crear las tablas en la base de datos si no existen
        db.create_all()

        # Insertar valores en la tabla de sexo si no existen
        if not Sexo.query.first():
            sexos = [
                Sexo(nombre='Masculino'),
                Sexo(nombre='Femenino'),
                Sexo(nombre='Otros')
            ]
            db.session.bulk_save_objects(sexos)
            db.session.commit()

        # Insertar valores en la tabla de tipo de documento si no existen
        if not TipoDocumento.query.first():
            tipos_documento = [
                TipoDocumento(nombre='Cédula de Identidad Paraguaya'),
                TipoDocumento(nombre='Pasaporte'),
                TipoDocumento(nombre='Cédula de Identidad Extranjera')
            ]
            db.session.bulk_save_objects(tipos_documento)
            db.session.commit()

        # Insertar valores en la tabla de tipo de personas si no existen
        if not TipoPersona.query.first():
            tipos_persona = [
                TipoPersona(nombre='Operador'),
                TipoPersona(nombre='Tutor'),
                TipoPersona(nombre='Profesor'),
                TipoPersona(nombre='Alumno')
            ]
            db.session.bulk_save_objects(tipos_persona)
            db.session.commit()

        # Insertar valores en la tabla de estado civil si no existen
        if not EstadoCivil.query.first():
            estados_civil = [
                EstadoCivil(nombre='Menor'),
                EstadoCivil(nombre='Soltero'),
                EstadoCivil(nombre='Casado'),
                EstadoCivil(nombre='Divorciado'),
                EstadoCivil(nombre='Viudo')
            ]
            db.session.bulk_save_objects(estados_civil)
            db.session.commit()

        # Insertar valores en la tabla de nacionalidad si no existen
        if not Nacionalidad.query.first():
            nacionalidades = [
                Nacionalidad(nombre='Argentina'),
                Nacionalidad(nombre='Bolivia'),
                Nacionalidad(nombre='Brasil'),
                Nacionalidad(nombre='Chile'),
                Nacionalidad(nombre='Colombia'),
                Nacionalidad(nombre='Costa Rica'),
                Nacionalidad(nombre='Cuba'),
                Nacionalidad(nombre='Ecuador'),
                Nacionalidad(nombre='El Salvador'),
                Nacionalidad(nombre='Guatemala'),
                Nacionalidad(nombre='Honduras'),
                Nacionalidad(nombre='México'),
                Nacionalidad(nombre='Nicaragua'),
                Nacionalidad(nombre='Panamá'),
                Nacionalidad(nombre='Paraguay'),
                Nacionalidad(nombre='Perú'),
                Nacionalidad(nombre='República Dominicana'),
                Nacionalidad(nombre='Uruguay'),
                Nacionalidad(nombre='Venezuela')
            ]
            db.session.bulk_save_objects(nacionalidades)
            db.session.commit()

        # Insertar valores en la tabla de roles si no existen
        if not Role.query.first():
            roles = [
                Role(nombre='Admin'),
                Role(nombre='Operador'),
                Role(nombre='Alumno'),
                Role(nombre='Profesor')
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()

        # Insertar personas "ADMIN" si no existe
        if not Persona.query.filter_by(nombres='ADMIN').first():
            admin_persona = Persona(
                nombres='ADMIN',
                apellidos='ADMIN',
                apellido_nombre='ADMIN',
                direccion='Calle Falsa 123',
                ciudad='Asunción',
                correo='admin@example.com',
                fecha_nacimiento='1980-01-01',  # Fecha aleatoria
                telefono=123456789,
                estado=1,  # Activo
                sexo_id=Sexo.query.filter_by(nombre='Masculino').first().id,
                nacionalidad_id=Nacionalidad.query.filter_by(nombre='Paraguay').first().id,
                estado_civil_id=EstadoCivil.query.filter_by(nombre='Soltero').first().id
            )
            db.session.add(admin_persona)
            db.session.commit()

        # Insertar usuario "admin" vinculado a la personas "ADMIN" y rol "Admin"
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('adminpassword'),
                role_id=Role.query.filter_by(nombre='Admin').first().id,
                persona_id=Persona.query.filter_by(nombres='ADMIN').first().id,
                estado=1  # Activo
            )
            db.session.add(admin_user)
            db.session.commit()

    return app
