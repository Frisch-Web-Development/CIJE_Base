
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required


db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), unique=False, index=True)
    last_name = db.Column(db.String(64), unique=False, index=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(64), unique=False, index=True)
    is_active = True

    def __repr__(self):
        return '<User %r>' % self.email


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, index=True)
    type = db.Column(db.String(64), unique=False, index=True)
    contact = db.Column(db.String(64), unique=False, index=True)
    long = db.Column(db.Float, unique=False)
    lat = db.Column(db.Float, unique=False)
    other = db.Column(db.Text, unique=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
       }

    def __init__(self, name, type, contact, lat, long, other):
        self.name = name
        self.type = type
        self.contact = contact
        self.lat = lat
        self.long = long
        self.other = other

