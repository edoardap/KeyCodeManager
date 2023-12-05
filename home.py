import cv2
import numpy as np
from pyzbar.pyzbar import decode
import keyboard
from classesV2 import *

from flask import Flask, render_template, request, redirect, send_file
app=Flask(__name__,template_folder='Templates',static_folder="static")

from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

adaptador_bd = adapterBD()
gerenciador = Gerenciador(adaptador_bd)
gerente = Gerente("Jeremias", "12345", "@gmail.com")
login = TelaLogin()
funcionario = Funcionario("", "", "", "" )


#Metodo para validar login
@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    login.email = request.form.get("email")
    login.senha = request.form.get("senha")
    amostra = supabase.table("usuarios").select('email', 'senha').eq("email", login.email).eq("senha", login.senha).execute()
    resp = supabase.table("usuarios").select('id').eq("email", login.email).eq("senha", login.senha).execute()
    if resp.data:
        login.id = resp.data[0].get('id')
        print(login.id)
    if amostra.data != []:
        if login.email == 'gerente@ifpb.edu.br':
            return render_template('tela-inicial.html')
        if login.email.endswith('@ifpb.edu.br'):
            return render_template('tela-inicial2.html')
        elif  login.email.endswith('@academico.ifpb.edu.br'):
            return render_template('tela-inicial3.html')
        else:
            '<h1> email ou senha incorretos </h1>'
    else:
        return '<h1> email ou senha incorretos </h1>'


@app.route("/home.html", methods = ["GET", "POST"])
def lerQRCODE(mirror=False):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    myData = None
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('Leitor', img)
        for barcode in decode(img):
            # print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print(myData, flush=True)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)
            if myData:
                break

        if cv2.waitKey(1) == 27 or myData:
            break
    cv2.destroyAllWindows()
    cam.release()
    chave = Chave(myData, "", "", "")
    resposta = funcionario.pegarChave(chave, login.id)
    if resposta == 2:
        return '<h1>Chave não cadastrada</h1>'
    else:
        return '<h1>Você pegou a chave {}!</h1>'.format(chave.getNomeSala())

#Retorna apenas o básico
@app.route("/acesso.html", methods = ["GET", "POST"])
def acessarChaves():
   chaves = gerente.AcessarChavesCadastradas(gerenciador)
   for chave in chaves.data:
       return render_template('acessar-chaves.html', chaves=chaves, retornarNomePeloID=retornarNomePeloID)

def retornarNomePeloID(id):
    user_name = supabase.table("usuarios").select('nome').eq("id", id).execute()
    name = user_name.data[0].get('nome')
    print(name)
    return name

@app.route("/gerar_qrcode/<cod>/<name>", methods=["GET", "POST"])
def gerar_qrcode(cod, name):
    gerador = geradorQRCode()
    img_path = gerador.gerarQRCode(cod, name)
    return send_file(img_path, as_attachment=True)

@app.route("/usuarios.html", methods = ["GET", "POST"])
def acessarUsuarios():
    if request.method == "GET":
      usuarios = supabase.table('usuarios').select('id','nome','email').execute()
      for usuario in usuarios.data:
         return render_template('acessar-usuarios.html', usuario = usuarios)

@app.route("/deleteUsuario/<id>", methods=["GET", "POST"])
def deleteUsuario(id):
    adapter = adapterBD()
    adapter.deleteUsuario(id)
    return '<h1> Usuário removido com sucesso </h1>'

@app.route('/chave.html')
def novaChave():
    return render_template('nova-chave.html')

@app.route('/adicionarChave', methods=['POST'])
def adicionarChave():
    # Obtenha os dados do formulário
    nome_sala = request.form['nomeSala']
    qr_code = request.form['qrCode']

    # Nome da tabela no Supabase
    tabela = 'chaves'

    # Verificar se o registro já existe (assumindo que 'ID' é uma chave única)
    registro_existente = supabase.table(tabela).select('nomeSala').eq('nomeSala', nome_sala).execute()


    if registro_existente.data !=[]:
        # Se o registro existir, você pode optar por atualizá-lo usando o método update
        supabase.table(tabela).update([{'nomeSala': nome_sala, 'qrCode': qr_code}]).eq('nomeSala', nome_sala).execute()
    else:
        resultados = supabase.table(tabela).select('id').order('id', desc=True).limit(1).single().execute()
        last_ID = resultados.data['id']+1
        # Se o registro não existir, insira um novo registro usando o método insert
        dados_para_adicionar = [{'id': last_ID, 'nomeSala': nome_sala, 'qrCode': qr_code}]
        resposta = supabase.table(tabela).insert(dados_para_adicionar).execute()
    return redirect('/chave.html')

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
