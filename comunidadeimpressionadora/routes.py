from flask import render_template, redirect, request, flash, url_for
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import User
from flask_login import login_user


lista_usuarios = ['Samuel', 'Joao']


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contato")
def contact():
    return render_template('contact.html')


@app.route("/lista-usuarios")
def users():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        user = User.query.filter_by(email= form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.senha.data):
            flash(f"Login feito com sucesso!Email: {form_login.email.data}", 'alert-success')
            login_user(user, remember=False)
            return redirect(url_for('home'))
        else:
            flash(f"Falha no login!Email ou senha incorreta", 'alert-danger')
        return redirect(url_for('home'))
    if form_criar_conta.validate_on_submit() and "botao_submit_criar_conta" in request.form:
        #criar o usuário
        password_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        user = User(username= form_criar_conta.username.data, email= form_criar_conta.email.data, password= password_crypt)
        database.session.add(user)
        database.session.commit()
        flash(f"Conta criada com sucesso!Email: {form_criar_conta.email.data}", 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)
