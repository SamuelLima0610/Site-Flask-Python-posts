from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import User

class FormCriarConta(FlaskForm):


    username = StringField("Nome do usuário: ", validators=[DataRequired()])
    email= StringField("Email: ", validators=[DataRequired(), Email()])
    senha= PasswordField("Senha: ", validators=[DataRequired(), Length(6,20)])
    confirmacao= PasswordField("Confirmação Senha: ", validators=[DataRequired(), EqualTo("senha")])
    botao_submit_criar_conta= SubmitField("Criar conta: ")


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(message="Email já cadastrado! Cadastra-se com outro email ou faça o login")


class FormLogin(FlaskForm):

    email = StringField("Email: ", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha: ", validators=[DataRequired(), Length(6,20)])
    lembra_dados = BooleanField("Lembra dados")
    botao_submit_login = SubmitField("Entrar")