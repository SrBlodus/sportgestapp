# persona_routes.py
from app import db


class Persona(db.Model):
    __tablename__ = 'personas'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(256), nullable=True)
    ciudad = db.Column(db.String(64), nullable=False)
    correo = db.Column(db.String(128), unique=True, nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.BigInteger, nullable=True)

    # Relaciones
    sexo_id = db.Column(db.Integer, db.ForeignKey('sexo.id'), nullable=True)
    nacionalidad_id = db.Column(db.Integer, db.ForeignKey('nacionalidad.id'), nullable=True)
    estado_civil_id = db.Column(db.Integer, db.ForeignKey('estado_civil.id'), nullable=True)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=True)

    # Relaciones inversas
    sexo = db.relationship('Sexo', backref='personas')
    nacionalidad = db.relationship('Nacionalidad', backref='personas')
    estado_civil = db.relationship('EstadoCivil', backref='personas')
    estado = db.relationship('Estado', backref='personas')

    def __repr__(self):
        return f'<Persona {self.nombres} {self.apellidos}>'
