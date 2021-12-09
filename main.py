from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

lista_usuarios = ['Alan', 'Samuel', 'Rafael']
app.config['SECRET_KEY'] = "16c6bcd635accdbec64dc90e8808d18b"
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contato")
def contact():
    return render_template('contact.html')

@app.route("/lista-usuarios")
def users():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/login", methods=["GET","POST"])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        flash(f"Login feito com sucesso!Email: {form_login.email.data}", 'alert-success')
        return redirect(url_for('home'))
    if form_criar_conta.validate_on_submit() and "botao_submit_criar_conta" in request.form:
        flash(f"Conta criada com sucesso!Email: {form_criar_conta.email.data}", 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


if __name__ == '__main__':
    app.run(debug=True)