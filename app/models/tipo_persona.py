#tipo_persona.py
from app import db


class TipoPersona(db.Model):
    __tablename__ = 'tipo_persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<TipoPersona {self.nombre}>'
