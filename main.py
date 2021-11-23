from flask import Flask, render_template

app = Flask(__name__)

lista_usuarios = ['Alan', 'Samuel', 'Rafael']

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contato")
def about():
    return render_template('about.html')

@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


if __name__ == '__main__':
    app.run(debug=True)