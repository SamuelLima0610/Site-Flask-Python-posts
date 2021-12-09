from main import database
from datetime import datetime


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    user_photo = database.Column(database.String, default='default.jpg', nullable=False)
    posts = database.relationship('Post', backref='owner', lazy=True)
    courses = database.Column(database.String, nullable=False, default='Não informado')


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    create_at = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

