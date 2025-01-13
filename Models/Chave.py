from Models.ChavePrototipo import ChavePrototipo
from flask import Blueprint, render_template, request, redirect, url_for
from supabase import create_client

supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

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

    # Nome da tabela no Supabase
    tabela = 'chaves'

    # Verificar se o registro já existe
    registro_existente = supabase.table(tabela).select('nomeSala').eq('nomeSala', nome_sala).execute()

    if registro_existente.data:
        # Atualizar o registro existente
        supabase.table(tabela).update({'nomeSala': nome_sala, 'qrCode': qr_code}).eq('nomeSala', nome_sala).execute()
    else:
        # Obter o último ID e adicionar um novo registro
        resultados = supabase.table(tabela).select('id').order('id', desc=True).limit(1).execute()
        last_ID = resultados.data[0]['id'] + 1 if resultados.data else 1
        dados_para_adicionar = [{'id': last_ID, 'nomeSala': nome_sala, 'qrCode': qr_code}]
        supabase.table(tabela).insert(dados_para_adicionar).execute()

    return redirect(url_for('chave.novaChave'))