import cv2
import numpy as np

import keyboard
from classesV2 import *
from Models.tela_login import TelaLogin
from Models.Chave import Chave
from Models.Chave import chave_bp
from Models.Usuario import Usuario
from Models.Funcionario import Funcionario
from Models.QrCode import QRCode, QRCode_bp
from Models.Aluno import Aluno
from Models.Professor import Professor
from Models.AdapterBD import adapterBD
from Models.Gerenciador import Gerenciador
from Models.Gerente import Gerente

from flask import Flask, render_template, request, redirect, send_file
app=Flask(__name__,template_folder='Templates',static_folder="static")

app.register_blueprint(chave_bp, url_prefix='/chave')
app.register_blueprint(QRCode_bp, url_prefix='/QRCode')


from dotenv import load_dotenv
from flask import session

load_dotenv()

import os
from supabase import create_client

supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

adaptador_bd = adapterBD()
gerenciador = Gerenciador(adaptador_bd)
gerente = Gerente("Jeremias", "12345", "@gmail.com")
loginVariavel = TelaLogin()
app.secret_key = '12345'

class AutenticadorReal:
    def validar_login(self, loginVariavel):
       # Usando os métodos getters da classe TelaLogin
       amostra = supabase.table("usuarios").select('email', 'senha').eq("email",loginVariavel.getEmail()).eq("senha", loginVariavel.getSenha()).execute()
       resp = supabase.table("usuarios").select('id').eq("email", loginVariavel.getEmail()).eq("senha", loginVariavel.getSenha()).execute()
       if resp.data:
            loginVariavel.setId(resp.data[0].get('id'))  # Usando o método setter para definir o id
            session['user_id'] = loginVariavel.getId()  # Salvando o id do usuário na sessão
       if amostra.data and resp.data:
           return True

class ProxyAutenticacao:
    def __init__(self):
        self.autenticador_real = AutenticadorReal()

    def validar_login(self, loginVariavel):
        # Passa o objeto 'login' para o método 'validar_login' da classe AutenticadorReal
        return self.autenticador_real.validar_login(loginVariavel)

proxy_autenticacao = ProxyAutenticacao()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    loginVariavel.setEmail(request.form.get("email"))
    loginVariavel.setSenha(request.form.get("senha"))

    if proxy_autenticacao.validar_login(loginVariavel):
        if loginVariavel.getEmail() == 'gerente@ifpb.edu.br':
            session['user_type'] = 'gerente'
            return render_template('tela-inicial.html')

        elif loginVariavel.getEmail().endswith('@ifpb.edu.br'):
            session['user_type'] = 'professor'
            return render_template('tela-inicial2.html')

        elif loginVariavel.getEmail().endswith('@academico.ifpb.edu.br'):
            session['user_type'] = 'aluno'
            return render_template('tela-inicial3.html')
        else:
            return '<h1> Email ou senha incorretos </h1>'
    else:
        return '<h1> Email ou senha incorretos 2</h1>'


@app.route("/acesso.html", methods = ["GET", "POST"])
def acessarChaves():
   chaves = gerente.AcessarChavesCadastradas(gerenciador)
   for chave in chaves.data:
       return render_template('acessar-chaves.html', chaves=chaves, retornarNomePeloID=retornarNomePeloID)

def retornarNomePeloID(id):
    user_name = supabase.table("usuarios").select('nome').eq("id", id).execute()
    name = user_name.data[0].get('nome')
    return name


@app.route("/usuarios.html", methods = ["GET", "POST"])
def acessarUsuarios():
    if request.method == "GET":
      usuarios = supabase.table('usuarios').select('id','nome','email').execute()
      for usuario in usuarios.data:
         return render_template('acessar-usuarios.html', usuario = usuarios)

@app.route("/deleteUsuario/<id>", methods=["GET", "POST"])
def deleteUsuario(id):
    gerenciador.removerUsuario(id)
    return '<h1> Usuário removido com sucesso </h1>'



@app.route('/addUsuario', methods=['POST'])
def adicionarUsuario():
    # Obtenha os dados do formulário
    email = request.form['logemail_c']
    nome = request.form['logname']
    senha = request.form['logpass']

    # Nome da tabela no Supabase
    tabela = 'usuarios'

    # Verificar se o registro já existe (assumindo que 'ID' é uma chave única)
    registro_existente = supabase.table(tabela).select('email').eq('email', email).execute()


    if registro_existente.data !=[]:
        # Se o registro existir, você pode optar por atualizá-lo usando o métod{{url_for('novaChave')}}o update
        supabase.table(tabela).update([{'nome': nome, 'email': email, 'senha' :senha}]).eq('email', email).execute()
    else:
        resultados = supabase.table(tabela).select('id').order('id', desc=True).limit(1).single().execute()
        last_ID = resultados.data['id']+1
        # Se o registro não existir, insira um novo registro usando o método insert
        dados_para_adicionar = [{'id': last_ID, 'nome': nome, 'email': email,'senha':senha}]
        resposta = supabase.table(tabela).insert(dados_para_adicionar).execute()
    return redirect('/')

@app.route("/acessarHistorico", methods = ["GET", "POST"])
def acessarHistorico():
    #query = """SELECT historico.hora,chaves.nomeChave,usuarios.nomeUsuario FROM historico JOIN chaves ON historico.idChave = chaves.id JOIN usuarios ON historico.idUsuario = usuarios.id;"""
    #controle = supabase.query(query)
    if request.method == 'GET':
        historicos = supabase.table('historico').select('id', 'hora', 'id_chave', 'id_usuario').execute()
#         id = historicos.data[0].get('id_chave')
#         retornarChavePeloID(id)

        for historico in historicos.data:
            return render_template('acessar-historico.html', historico=historicos)

def retornarChavePeloID(id):
      chave = supabase.table('chaves').select('nomeSala').eq("id", id).execute()
      nomeSala = chave.data[0].get('nomeSala')
      return nomeSala

if __name__ == "__main__":
    app.run(debug=True)