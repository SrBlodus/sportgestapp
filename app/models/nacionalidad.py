# nacionalidad.py
from app import db

class Nacionalidad(db.Model):
    __tablename__ = 'nacionalidad'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Nacionalidad {self.nombre}>'

