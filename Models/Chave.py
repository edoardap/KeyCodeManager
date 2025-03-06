from Models.ChavePrototipo import ChavePrototipo
from flask import Blueprint, render_template, request, redirect, url_for

from api.AdapterDB import AdapterDB
adapter = AdapterDB(host="localhost", user="manager", password="K@qr0208", database="keycode")

# Criando um Blueprint para as rotas relacionadas a "Chave"
chave_bp = Blueprint('chave', __name__, template_folder='../Templates')

class Chave(ChavePrototipo):
    def __init__(self, id_chave, nome, qr_code, posse):
        super().__init__(id_chave, nome, qr_code, posse)

    def setId(self, id_chave):
        self._idChave = id_chave

    def setNomeSala(self, nome):
        self._nomeSala = nome

    def setQrCode(self, cod):
        self._qrCode = cod

    def setPosse(self, id):
        self._posse = id

    def setAtivo(self, ativo):
        self._ativo = ativo

    def getId(self):
        return self._idChave  # Corrigido para acessar o atributo correto

    def getNomeSala(self):
        return self._nomeSala  # Corrigido para acessar o nome da sala

    def getQrCode(self):
        return self._qrCode

    def getPosse(self):
        return self._posse


@chave_bp.route('/chave.html')
def novaChave():
    return render_template('nova-chave.html')

# Rota para adicionar uma nova chave
@chave_bp.route('/adicionarChave', methods=['POST'])
def adicionarChave():
    # Obtenha os dados do formulário
    nome_sala = request.form['nomeSala']
    qr_code = request.form['qrCode']

    # Verificar se o registro já existe no banco
    chave_existente = adapter.get_chaves(nome = nome_sala)

    if chave_existente:
        # Atualizar o registro existente
        query = "UPDATE chaves SET nome = %s, qrcode = %s WHERE nomeSala = %s"
        params = (nome_sala, qr_code, nome_sala)
        adapter.execute_query(query, params)
    else:
        # Inserir novo registro
        adapter.add_chave(nome_sala, qr_code)

    return redirect(url_for('acessarChaves')), 303
