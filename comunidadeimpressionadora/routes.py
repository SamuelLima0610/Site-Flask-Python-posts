import secrets
import os
from flask import render_template, redirect, request, flash, url_for
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditPerfil
from comunidadeimpressionadora.models import User
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contato")
def contact():
    return render_template('contact.html')


@app.route("/lista-usuarios")
@login_required
def users():
    lista_usuarios = User.query.all()
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
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
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


@app.route("/perfil")
@login_required
def perfil():
    image_perfil = url_for('static', filename=f'imgs_perfil/{current_user.user_photo}')
    return render_template('perfil.html', image_perfil=image_perfil)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Saída com sucesso!", 'alert-success')
    return redirect(url_for('home'))


@app.route("/post/create")
@login_required
def create_post():
    return render_template('createpost.html')


def save_image(image):
    # adicionar um código aleatório
    code = secrets.token_hex(8)
    name, extension = os.path.splitext(image.filename)
    name_file = name + code + extension
    path_file = os.path.join(app.root_path, 'static/imgs_perfil', name_file)
    # reduzir o tamanho da imagem
    size = (200, 200)
    reduce_image = Image.open(image)
    reduce_image.thumbnail(size)
    reduce_image.save(path_file)
    # salvar a imagem no diretório
    return name_file


def atualize_courses(form):
    course_list = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                course_list.append(campo.label.text)
    if len(course_list) == 0:
        return 'Não informado'
    return ';'.join(course_list)

@app.route("/perfil/editar", methods=["GET", "POST"])
def edit_perfil():
    form = FormEditPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.user_photo.data:
            image = save_image(form.user_photo.data)
            current_user.user_photo = image
        current_user.courses = atualize_courses(form)
        database.session.commit()
        flash(f"Perfil atualizado com sucesso!Email: {form.email.data}", 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    image_perfil = url_for('static', filename=f'imgs_perfil/{current_user.user_photo}')
    return render_template('editperfil.html', image_perfil=image_perfil, form=form)

