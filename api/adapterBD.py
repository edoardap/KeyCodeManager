import classes
from datetime import date, time, datetime

from supabase import create_client
supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

class adapterBD:
    def __init__(self):
        pass

    def readChave(self, chave):
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("id", chave.getId()).execute()
        if table.data != []:
            chave.setNomeSala(table.data[0]['nomeSala'])
            chave.setQrCode(table.data[0]['qrCode'])
            chave.setPosse(table.data[0]['posse'])
            return chave
        else:
            return chave

    def readFuncionario(self, usuario):
        table = supabase.table("usuarios").select('*').eq("email", usuario.getEmail()).execute()
        if table.data != []:
            usuario.setId(table.data[0]['id'])
            usuario.setNome(table.data[0]['nome'])
            usuario.setSenha(table.data[0]['senha'])
            return usuario
        else:
            return usuario

    def readAluno(self, aluno):
        table = supabase.table("usuarios").select('*').eq("email", aluno.getEmail()).execute()
        list = []
        if table.data != []:
            aluno.setId(table.data[0]['id'])
            aluno.setNome(table.data[0]['nome'])
            aluno.setSenha(table.data[0]['senha'])
            table2 = supabase.table("alunos").select('*').eq("usuario_id", table.data[0]['id']).execute()
            if table2.data != []:
                aluno.setMatricula(table2.data[0]['matricula'])
                table3 = supabase.table("alunos_chaves").select('chave_id').eq("aluno_id", table2.data[0]['id']).execute()
                if table3.data != []:
                    for i in range(0,len(table3.data)):
                        list.append(table3.data[i]['chave_id'])
                    aluno.setListChaves(list)

        return aluno

    def readHistorico(self, modo = 'completo', datainicial = 0, datafinal = 0):
        if modo == 'completo':
            table = supabase.table("historico").select('*').execute()

        elif modo == 'periodo':
            table = supabase.table("historico").select('*').gte('hora', datainicial).lte('hora', datafinal).execute()

        return table.data

    def writeHistorico(self, chave, usuario):
        supabase.table("historico").insert(
            {"hora":str(datetime.now()), "id_chave":chave.getId(), "id_usuario":usuario.getId()}).execute()
        return self

    def writeChave(self,chave):
        supabase.table('chave').insert(
            {'nomeSala':chave.getNomeSala(), "qrCode":chave.getQrCode(), "posse":chave.getPosse()}).execute()
        return self

    def writeAlunoChave(self, aluno, chave, professor):
        supabase.table('alunos_chaves').insert(
            {'chave_id': chave.getId(), "aluno_id": aluno.getId(), "responsavel": professor.getId()}).execute()
        return self

    def writeUsuario(self,usuario):
        supabase.table('usuario').insert(
            {'nome': usuario.getNome(), 'email': usuario.getEmail(), 'senha': usuario.getSenha()}).execute()
        return self

    def writeAluno(self,aluno):
        self.writeUsuario(aluno)
        supabase.table('aluno').insert(
            {'usuario_id':aluno.getId(), 'matricula': aluno.getMatricula()}).execute()
        return self

    def writeFuncionario(self,funcionario):
        self.writeUsuario(funcionario)
        supabase.table('funcionario').insert(
            {'usuario_id': funcionario.getId()}).execute()
        return self

    def writeProfessor(self,professor):
        self.writeUsuario()
        self.writeFuncionario()
        table = supabase.table("funcionarios").select('id').eq("usuario_id", professor.getId()).execute()
        supabase.table('professores').insert(
            {'funcionario_id': table.data[0]['id']}).execute()
        return self

    def writeGerente(self,gerente):
        self.writeUsuario()
        self.writeFuncionario()
        table = supabase.table("funcionarios").select('id').eq("usuario_id", gerente.getId()).execute()
        supabase.table('gerentes').insert(
            {'funcionario_id': table.data[0]['id']}).execute()
        return self

