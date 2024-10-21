#estado_civil.py
from app import db

class EstadoCivil(db.Model):
    __tablename__ = 'estado_civil'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<EstadoCivil {self.nombre}>'