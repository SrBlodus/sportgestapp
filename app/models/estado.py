#estado.py
from app import db

class Estado(db.Model):
    __tablename__ = 'estado'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<Estados {self.nombre}>'