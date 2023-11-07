from flask import Flask, render_tamplate, request, redirect, session
import sqlite3 as sql
import uuid

app = Flask(__name__)
app.secret_key = "carioca"

usuario = "usuario"
senha = "senha"
login = False

#FUNÇÃO PARA VERIFICAR SESSÃO 
def verificar_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False 

#CONEXÃO COM O BANCO DE DADOS
def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao 

#INICIAR O BANCO DE DADOS
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()

#ROTA DA PÁGINA INICIAL- Definir iniciar_db inicializar esquema.sql
@app.route('/')
def index():
    iniciar_db() #chamando o BD
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", produtos=produtos, title=title)

#FINAL DO CÓDIGO
app.run(debug=True)