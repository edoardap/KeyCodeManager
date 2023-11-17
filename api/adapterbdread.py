import classes
from datetime import date, time, datetime

from supabase import create_client
supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

class adapterBDread:
    def __init__(self):
        pass

    def readChave(self, chave):
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("id", chave.getId()).execute()
        if table.data != []:
            chave.setNomeSala(table.data[0]['nomeSala'])
            chave.setqrCode(table.data[0]['qrCode'])
            chave.setposse(table.data[0]['posse'])
            return chave
        else:
            return chave

    def readFuncionario(self, usuario):
        table = supabase.table("usuarios").select('*').eq("email", usuario.getEmail()).execute()
        if table.data != []:
            usuario.setNome(table.data[0]['nome'])
            usuario.setSenha(table.data[0]['senha'])
            return usuario
        else:
            return usuario

    def readAluno(self, aluno):
        table = supabase.table("usuarios").select('*').eq("email", aluno.getEmail()).execute()
        list = []
        if table.data != []:
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






