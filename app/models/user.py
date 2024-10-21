#user.py
from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    estado = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
