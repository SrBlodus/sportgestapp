#tipo_documento.py
from app import db

class TipoDocumento(db.Model):
    __tablename__ = 'tipo_documento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<TipoDocumento {self.nombre}>'
