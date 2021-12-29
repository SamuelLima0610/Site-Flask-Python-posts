from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "16c6bcd635accdbec64dc90e8808d18b"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
bcrypt = Bcrypt(app)

database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, realize o login!'
login_manager.login_message_category = 'alert-info'


from comunidadeimpressionadora import routes