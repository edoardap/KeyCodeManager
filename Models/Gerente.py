from Models.Funcionario import Funcionario
from supabase import create_client
supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)
from flask import render_template, url_for


class Gerente(Funcionario):
    def __init__(self, nome="", senha="", email="", contrato="", id=""):
        super().__init__(nome, senha, email, contrato)
        self._id = id

    def setId(self, num):
        self._id = num

    def gerarQrCode(self, gerador):
        pass

    def cadastrarChave(self, chave, gerenciador):
        gerenciador.cadastrarChave(chave)

    def modificarChave(self, chave, gerenciador):
        gerenciador.alterarChave(chave)


    def removerChave(self, chave, gerenciador):
        gerenciador.removerChave(chave)
        pass

    def AcessarChavesCadastradas(self, gerenciador):
        return gerenciador.acessarChaves()

    def adicionarUsuario(self, usuario, gerenciador):
        gerenciador.adicionarUsuario(usuario)

    def modificarUsuario(self, usuario, gerenciador):
        gerenciador.alterarUsuario(usuario)

    def removerUsuario(self, usuario, gerenciador):
        gerenciador.removerUsuario(usuario)

    def pegarChave(self, chave, id_user):
        print('chave', chave.getQrCode())
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("qrCode", chave.getQrCode()).execute()
        if chave.getQrCode() == '5':
            table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("qrCode", 'Laboratório de Informática 5').execute()

        print()
        if table.data != []:
            chave.setId( table.data[0]['id'])
            chave.setNomeSala(table.data[0]['nomeSala'])
            chave.setQrCode(table.data[0]['qrCode'])
            chave.setPosse(table.data[0]['posse'])
            supabase.table('chaves').update([{'posse': id_user}]).eq('id', chave.getId()).execute()
            return render_template('chavePega.html', nome_sala=chave.getNomeSala(), tipoUser='/tela-inicial')
        else:
            return '<h1>Chave não cadastrada</h1>'

