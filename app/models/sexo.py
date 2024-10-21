#sexo.py
from app import db

class Sexo(db.Model):
    __tablename__ = 'sexo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f'<Sexo {self.nombre}>'
