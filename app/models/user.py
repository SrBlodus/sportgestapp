#user.py
from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    # Relaciones
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=True)
    # Relaciones inversas
    estado = db.relationship('Estado', backref='user')

    def __repr__(self):
        return f'<User {self.username}>'
