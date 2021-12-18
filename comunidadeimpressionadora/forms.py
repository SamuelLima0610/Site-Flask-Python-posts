from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import User
from flask_login import current_user


class FormCriarConta(FlaskForm):


    username = StringField("Nome do usuário: ", validators=[DataRequired()])
    email= StringField("Email: ", validators=[DataRequired(), Email()])
    senha= PasswordField("Senha: ", validators=[DataRequired(), Length(6,20)])
    confirmacao= PasswordField("Confirmação Senha: ", validators=[DataRequired(), EqualTo("senha")])
    botao_submit_criar_conta= SubmitField("Criar conta")


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(message="Email já cadastrado! Cadastra-se com outro email ou faça o login")


class FormLogin(FlaskForm):

    email = StringField("Email: ", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha: ", validators=[DataRequired(), Length(6,20)])
    lembra_dados = BooleanField("Lembra dados")
    botao_submit_login = SubmitField("Entrar")


class FormEditPerfil(FlaskForm):

    username = StringField("Nome do usuário: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    user_photo = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel = BooleanField("Excel")
    curso_vba = BooleanField("Vba")
    curso_python = BooleanField("Python")
    curso_powerbi = BooleanField("Power Bi")
    botao_submit_perfil= SubmitField("Confirmar Edição")


    def validate_email(self, email):
        # verificar se o email mudou
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(message="Email já cadastrado!")


class FormCriarPost(FlaskForm):

    title= StringField("Título do Post", validators=[DataRequired(), Length(3,140)])
    body= TextAreaField("Escreva seu post aqui!", validators=[DataRequired()])
    botao_submit_post = SubmitField("Criar Post")