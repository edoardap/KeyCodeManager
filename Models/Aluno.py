from Models.Usuario import Usuario
from supabase import create_client
supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

class Aluno(Usuario):
    def __init__(self, nome, senha, email, matricula):
        super().__init__(nome, senha, email)
        self._matricula = matricula
        self._listChaves = []

    def setMatricula(self, matricula):
        self._matricula = matricula

    def getMatricula(self):
        return self._matricula

    def adicionarChave(self, chave):
        pass

    def retornarChave(self, id_chave):
        pass

    def removerChave(self, chave):
        self._listChaves.remove(chave)

    def acessarChaves(self):
        for i in self._listChaves:
            pass

    def setListChaves(self, lista):
        self._listChaves = lista

    def passarChaveAluno(self, chave, aluno):
        pass

    def passarChave(self, funcionario):
        pass

    def pegarChave(self, chave, id_user):
        print('chave', chave.getQrCode())
        print('user', id_user)
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("qrCode",
                                                                                        chave.getQrCode()).execute()
        print('oi', table.data)
        print('chave.getId()', table.data[0]['id'])
        if table.data != []:
            chave.setId(table.data[0]['id'])
            chave.setNomeSala(table.data[0]['nomeSala'])
            chave.setQrCode(table.data[0]['qrCode'])
            chave.setPosse(table.data[0]['posse'])
            supabase.table('chaves').update([{'posse': id_user}]).eq('id', chave.getId()).execute()
            return chave
        else:
            return 2