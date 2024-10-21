#tutores.py
from app import db

class Tutor(db.Model):
    __tablename__ = 'tutores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)

    # Relaciones
    alumno = db.relationship('Persona', foreign_keys=[alumno_id], backref='alumnos')
    persona = db.relationship('Persona', foreign_keys=[persona_id], backref='tutores')

    def __repr__(self):
        return f'<Tutor {self.persona.apellidos}, Alumno {self.alumno.apellidos}>'

