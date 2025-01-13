from flask import request
from supabase import create_client

supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

class Gerenciador():
    _instancia = None
    def __init__(self, adaptador):
        if Gerenciador._instancia != None:
            raise Exception("This class is a singleton class!")
        else:
            self._gerenteChaves = ""
            Gerenciador._instancia = self
            self.adaptador = adaptador

    @staticmethod
    def getInstance():
        with Gerenciador._lock:
            if Gerenciador._instancia is None:
                return Gerenciador()
            return Gerenciador._instancia

    def adicionarUsuario(self, usuario):
        self.adaptador.writeUsuario(usuario)

    def removerUsuario(self, id):
        self.adaptador.deleteUsuario(id)

    def alterarUsuario(self, usuario):
        self.adaptador.updateUsuario(usuario)

    def cadastrarChave(self, chave):
        self.adaptador.writeChave(chave)

    def removerChave(self, chave):
        self.adaptador.deleteChave(chave)

    def alterarChave(self, chave):
        self.adaptador.updateChave(chave)

    def pegarChave(self, chave, id_user):
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("qrcode", chave.getQrCode()).execute()
        if table.data != []:
            chave.setId(table.data[0]['id'])
            chave.setNomeSala(table.data[0]['nomeSala'])
            chave.setQrCode(table.data[0]['qrCode'])
            chave.setPosse(table.data[0]['posse'])
            supabase.table('chaves').update([{'posse': id_user}]).eq('id', chave.getId()).execute()
            return chave
        else:
            return 2

    def acessarChaves(self):
        if request.method == "GET":
            return supabase.table('chaves').select('id', 'nomeSala', 'qrCode', 'posse').execute()


    def setGerente(self, gerente):
        self.adaptador.writeGerente(gerente)

    def getGerente(self):
        return self._gerenteChaves

    def removerGerente(self, gerente):
        self.adaptador.deleteGerente(gerente)

    def modificargerente(self, gerente):
        self.adaptador.updateGerente()