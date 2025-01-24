from Models.Usuario import Usuario
from flask import Blueprint
QRCode_bp = Blueprint('QRCode', __name__, template_folder='../Templates')

from supabase import create_client
supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

class Funcionario(Usuario):
    def __init__(self, nome, senha, email, contrato=""):
        super().__init__(nome, senha, email)
        self._contrato = contrato

    def setContrato(self, tipo):
        self._contrato = tipo

    def getContrato(self):
        return self._contrato

    def pegarChave(self, chave, id_user):
        print('chave', chave.getQrCode())
        print('user', id_user)
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("qrCode", chave.getQrCode()).execute()
        print('oi',table.data)
        print('chave.getId()', table.data[0]['id'])
        if table.data != []:
            chave.setId( table.data[0]['id'])
            chave.setNomeSala(table.data[0]['nomeSala'])
            chave.setQrCode(table.data[0]['qrCode'])
            chave.setPosse(table.data[0]['posse'])
            supabase.table('chaves').update([{'posse': id_user}]).eq('id', chave.getId()).execute()
            return chave
        else:
            return 2

    def passarChave(self, funcionario):
        pass

    def passarChaveAluno(self, chave, aluno):
        pass
