#personas_x_tipodoc.py
from app import db

class PersonaXTipoDoc(db.Model):
    __tablename__ = 'persona_x_tipodoc'

    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), primary_key=True)
    tipo_documento_id = db.Column(db.Integer, db.ForeignKey('tipo_documento.id'), primary_key=True)
    nro_documento = db.Column(db.String(45), nullable=False)

    persona = db.relationship('Persona', backref='documentos')
    tipo_documento = db.relationship('TipoDocumento')

    def __repr__(self):
        return f'<PersonaXTipoDoc {self.nro_documento}>'
