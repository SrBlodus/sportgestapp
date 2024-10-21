#persona_x_tipo.py
from app import db


class PersonaXTipo(db.Model):
    __tablename__ = 'persona_x_tipo'

    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    tipo_persona_id = db.Column(db.Integer, db.ForeignKey('tipo_persona.id'), nullable=False)

    persona = db.relationship('Persona', backref='tipos')
    tipo_persona = db.relationship('TipoPersona', backref='personas')

    def __repr__(self):
        return f'<PersonaXTipo {self.persona_id} - {self.tipo_persona_id}>'
