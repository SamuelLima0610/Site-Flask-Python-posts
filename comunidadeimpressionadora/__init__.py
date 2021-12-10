from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

lista_usuarios = ['Alan', 'Samuel', 'Rafael']
app.config['SECRET_KEY'] = "16c6bcd635accdbec64dc90e8808d18b"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
bcrypt = Bcrypt(app)

database = SQLAlchemy(app)
login_manager = LoginManager(app)


from comunidadeimpressionadora import routes