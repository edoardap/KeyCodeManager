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
from api.AdapterDB import AdapterDB

from flask import Flask, render_template, request, redirect, send_file, jsonify

app=Flask(__name__,template_folder='Templates',static_folder="static")

app.register_blueprint(chave_bp, url_prefix='/chave')
app.register_blueprint(QRCode_bp)

from dotenv import load_dotenv
from flask import session

load_dotenv()

adapter = AdapterDB(host="localhost", user="manager", password="K@qr0208", database="keycode")
gerenciador = Gerenciador(adapter)
gerente = Gerente("Jeremias", "12345", "@gmail.com")
loginVariavel = TelaLogin()
app.secret_key = '12345'

class AutenticadorReal:
    def validar_login(self, loginVariavel):
        # Buscar usuário no banco pelo email
        usuarios = adapter.get_usuarios(email=loginVariavel.getEmail())

        if usuarios:
            usuario = usuarios[0]  # Pegamos o primeiro usuário encontrado

            # Verifica se a senha está correta
            if usuario["senha"] == loginVariavel.getSenha():
                loginVariavel.setId(usuario["id"])  # Define o ID do usuário
                session['user_id'] = loginVariavel.getId()  # Salva o ID na sessão
                return True

        return False  # Retorna False se o login falhar

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
        if loginVariavel.getEmail() == 'gerencia@email.com':
            session['user_type'] = 'gerente'
            return render_template('tela-inicial.html')

        elif loginVariavel.getEmail().endswith('@ifpb.edu.br'):
            session['user_type'] = 'professor'
            return render_template('tela-inicial2.html')

        elif loginVariavel.getEmail().endswith('@academico.ifpb.edu.br'):
            session['user_type'] = 'aluno'
            return render_template('tela-inicial3.html')

    return '<h1>Email ou senha incorretos</h1>'

@app.route("/tela-inicial", methods=["GET"])
def telaInicialGerente():
    return render_template('tela-inicial.html')

@app.route("/tela-inicial2", methods=["GET"])
def telaInicialProfessor():
    return render_template('tela-inicial2.html')

@app.route("/tela-inicial3", methods=["GET"])
def telaInicialAluno():
    return render_template('tela-inicial3.html')

@app.route("/acesso.html", methods = ["GET", "POST"])
def acessarChaves():
    adapter.connection.commit()
    chaves = adapter.get_chaves()
    return render_template('acessar-chaves.html', chaves=chaves)

@app.route("/usuarios.html", methods = ["GET", "POST"])
def acessarUsuarios():
    if request.method == "GET":
      usuarios = adapter.get_usuarios()
      return render_template('acessar-usuarios.html', usuario = usuarios)

@app.route("/deleteUsuario/<id>", methods=["GET", "POST"])
def deleteUsuario(id):
    adapter.remove_usuario(id)
    return render_template('usuario-removido.html')

@app.route("/novoUsuario", methods=["GET", "POST"])
def novoUsuario():
    return render_template('novo-usuario.html')

@app.route('/adicionarUsuario', methods=['POST'])
def adicionarUsuario():
    # Obtenha os dados do formulário
    email = request.form['email']
    nome = request.form['nome']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmarSenha']
    tipo_usuario = request.form['tipoUsuario']
    matricula = request.form.get('matricula') or None  # Converte string vazia para None
    telefone = request.form.get('telefone') or None    # Converte string vazia para None

    # Verificar se as senhas coincidem
    if senha != confirmar_senha:
        return "Erro: As senhas não coincidem.", 400

    # Verificar se o usuário já existe
    usuario_existente = adapter.get_usuarios(email=email)
    if usuario_existente:
        # Atualizar os dados do usuário se já existir
        query = "UPDATE usuarios SET nome = %s, senha = %s, nivel = %s, matricula = %s, telefone = %s WHERE email = %s"
        params = (nome, senha, tipo_usuario, matricula, telefone, email)
        adapter.execute_query(query, params)
    else:
        # Inserir novo usuário
        adapter.add_usuario(nome, email, senha, tipo_usuario, matricula, telefone)

    return redirect('/tela-inicial')  # Redirecionar para a página inicial após o cadastro

@app.route("/alunosAutorizados", methods=["GET", "POST"])
def alunosAutorizados():
    professor_id = session.get('user_id')  # Obtém o ID do professor logado
    print(professor_id)
    alunos_autorizados = adapter.obter_alunos_autorizados(professor_id)
    return render_template('Alunos-autorizados.html', alunos_autorizados=alunos_autorizados)

@app.route("/acessarHistorico", methods=["GET", "POST"])
def acessarHistorico():
    adapter.connection.commit()

    # Parâmetros que podem ser passados pela requisição
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')
    hora_inicio = request.args.get('hora_inicio', '')
    hora_fim = request.args.get('hora_fim', '')
    chave = request.args.get('chave', 0, type=int)
    usuario_origem = request.args.get('usuario_origem', 0, type=int)
    usuario_destino = request.args.get('usuario_destino', 0, type=int)

    # Chama a função para obter o histórico
    historicos = adapter.get_historico(
        data_inicio=data_inicio,
        data_fim=data_fim,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        chave=chave,
        usuario_origem=usuario_origem,
        usuario_destino=usuario_destino
    )

    # Renderiza o template com os históricos encontrados
    return render_template('acessar-historico.html', historicos=historicos)


@app.route('/api/dados-graficos')
def obter_dados():
    adapter = AdapterDB(host="localhost", user="manager", password="K@qr0208", database="keycode")
    cursor = adapter.connection.cursor()  # Conectar corretamente

    # 1️⃣ Contar chaves totais
    cursor.execute("SELECT COUNT(*) FROM chaves")
    resultado = cursor.fetchone()

    total_chaves = resultado.get('COUNT(*)', 0)  # Retorna 0 se a chave não existir

    # 2️⃣ Contar usuários por categoria
    cursor.execute("SELECT nivel, COUNT(*) FROM usuarios GROUP BY nivel")
    usuarios = cursor.fetchall()

    categorias = [row["nivel"] for row in usuarios]  # Níveis de usuário
    valores = [row["COUNT(*)"] for row in usuarios]  # Quantidade por nível

    # Buscar as 5 chaves mais acessadas e seus nomes
    cursor.execute("""
        SELECT chaves.nome, COUNT(historico.id) AS quantidade
        FROM historico
        JOIN chaves ON historico.chave = chaves.id
        GROUP BY chaves.nome
        ORDER BY quantidade DESC
        LIMIT 5
    """)
    chaves_acessadas = cursor.fetchall()

    nomes_chaves = [row["nome"] for row in chaves_acessadas]  # Agora pega o nome real da chave
    quantidades = [row["quantidade"] for row in chaves_acessadas]  # Quantidade de acessos
    # Fechar conexões
    cursor.close()
    adapter.connection.close()  # Fechar a conexão corretamente

    return jsonify({
        "total_chaves": total_chaves,
        "usuarios": {"categorias": categorias, "valores": valores},
        "chaves_acessadas": {"nome": nomes_chaves, "quantidades": quantidades}
    })

@app.route('/acessarGraficos', methods=['GET', 'POST'])
def acessarGraficos():
    return render_template('graficos.html')

if __name__ == "__main__":
    app.run(debug=True)