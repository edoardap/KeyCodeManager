class adapterBD:
    def __init__(self):
        pass

    def readChave(self, chave):
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("id", chave).execute()
        if table.data != []:

            return Chave(chave, table.data[0]['nomeSala'], table.data[0]['qrCode'], table.data[0]['posse'])
        else:
            return []
    def readAlunoChave(self, aluno = 0, chave = 0, professor = 0):
        data = []

        if aluno != 0 and chave != 0 and professor != 0:
            table = supabase.table("alunos_chaves").select('*').eq('aluno_id', aluno, 'chave_id', chave, 'responsavel',professor).execute()
            data.append(table.data)

        elif aluno != 0 and chave != 0:
            table = supabase.table("alunos_chaves").select('*').eq('aluno_id', aluno, 'chave_id', chave).execute()
            data.append(table.data)

        elif aluno != 0 and professor != 0:
            table = supabase.table("alunos_chaves").select('*').eq('aluno_id', aluno, 'responsavel',professor).execute()
            data.append(table.data)

        elif  chave != 0 and professor != 0:
            table = supabase.table("alunos_chaves").select('*').eq('chave_id', chave, 'responsavel',professor).execute()
            data.append(table.data)

        elif aluno != 0:
            table = supabase.table("alunos_chaves").select('*').eq('aluno_id',aluno).execute()
            data.append(table.data)

        elif chave != 0:
            table = supabase.table("alunos_chaves").select('*').eq('chave_id',chave).execute()
            data.append(table.data)

        elif professor != 0:
            table = supabase.table("alunos_chaves").select('*').eq('responsavel',professor).execute()
            data.append(table.data)
        return data


    def readFuncionario(self, email):
        table = supabase.table("usuarios").select('*').eq("email", email).execute()
        if table.data != []:
            return Funcionario(table.data[0]['id'], table.data[0]['nome'], table.data[0]['senha'], email, 0)
        else:
            return []

    def readProfessor(self, email):
        table = supabase.table("usuarios").select('*').eq("email", email).execute()
        if table.data != []:
            return Professor(table.data[0]['id'], table.data[0]['nome'], table.data[0]['senha'], email, 0)
        else:
            return []

    def readGerente(self, email):
        table = supabase.table("usuarios").select('*').eq("email", email).execute()
        if table.data != []:
            return Gerente(table.data[0]['nome'], table.data[0]['senha'], email, 0, table.data[0]['id'])
        else:
            return []

    def readAluno(self, email):
        table = supabase.table("usuarios").select('*').eq("email", email).execute()
        list = []
        if table.data != []:
            id = table.data[0]['id']
            nome = table.data[0]['nome']
            senha = table.data[0]['senha']
            table2 = supabase.table("alunos").select('*').eq("usuario_id", id).execute()
            if table2.data != []:
                matricula = table2.data[0]['matricula']
                table3 = supabase.table("alunos_chaves").select('chave_id').eq("aluno_id", table2.data[0]['id']).execute()
                if table3.data != []:
                    for i in range(0,len(table3.data)):
                        list.append(table3.data[i]['chave_id'])

                return Aluno(id,nome,senha,email,matricula)
        return []

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

    def updateUsuario(self, usuario):
        supabase.table('usuarios').update(
            {'nome': usuario.getNome(), "email": usuario.getEmail(), "senha": usuario.getSenha()}
        ).eq('id',usuario.getId()).execute()

    def updateAluno(self, aluno):
        self.updateUsuario(aluno)
        supabase.table('alunos').update(
            {'matricula': aluno.getMatricula()}
        ).eq('usuario_id', aluno.getId()).execute()

    def updateAlunoChave(self, id, aluno, chave, professor):
        supabase.table('alunos_chaves').update(
            {'chave_id': chave.getId(), "aluno_id": aluno.getId(), "responsavel": professor.getId()}
        ).eq('id', id).execute()

    def updateChave(self,chave):
        supabase.table('chaves').update(
            {'nomeSala':chave.getNomeSala(), "qrCode":chave.getQrCode(), "posse":chave.getPosse()}
        ).eq('id', chave.getId()).execute()

    def updateFuncionario(self, funcionario):
        self.updateUsuario(funcionario)

    def updateGerente(self, gerente):
        self.updateUsuario(gerente)

    def updateProfessor(self, professor):
        self.updateUsuario(professor)

    def deleteAlunoChave(self,id):
        supabase.table('alunos_chaves').delete().eq('id', id).execute()

    def deleteChave(self,chave):
        supabase.table('chaves').delete().eq('id', chave.getId()).execute()

    def deleteUsuario(self, id):
        supabase.table('usuarios').delete().eq('id', id).execute()

    def deleteAluno(self, aluno):
        self.deleteUsuario(aluno)

    def deleteFuncionario(self, funcionario):
        self.deleteUsuario(funcionario)

    def deleteGerente(self, gerente):
        self.deleteUsuario(gerente)

    def deleteProfessor(self, professor):
        self.deleteUsuario(professor)