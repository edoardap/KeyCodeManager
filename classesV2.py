from supabase import create_client

supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)
from flask import Flask, render_template, request, redirect
app=Flask(__name__,template_folder='Templates',static_folder="static")
import os
class TelaLogin():
    def __init__(self, email="", senha="", nome=""):
        self.email = email
        self.senha = senha
        self.nome = nome
        self.id = ""

    def setEmail(self, email):
        self.email = email

    def setSenha(self, password):
        self.senha = password

    def setNome(self, nome):
        self.nome = nome

    def setId(self, id):
        self.id = id

    def getEmail(self):
        return self.email

    def getSenha(self):
        return self.senha

    def getNome(self):
        return self.nome

    def getId(self):
        return self.id

class Gerenciador():
    _instancia = None
    def __init__(self):
        if Gerenciador._instancia != None:
            raise Exception("This class is a singleton class!")
        else:
            self._gerenteChaves = ""
            Gerenciador._instancia = self

    @staticmethod
    def getInstance():
        with Gerenciador._lock:
            if Gerenciador._instancia is None:
                return Gerenciador()
            return Gerenciador._instancia

    def adicionarUsuario(self, usuario):
        self._usuarios.append(usuario)
        #chamada ao banco

    def removerUsuario(self, usuario):
        pass
        #chamada ao banco

    def alterarUsuario(self, usuario):
        pass

    def cadastrarChave(self, chave):
        pass

    def removerChave(self, chave):
        pass

    def alterarChave(self):
        pass

    def pegarChave(self, chave, id_user):
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("id", chave.getId()).execute()
        print(table.data)
        if table.data != []:
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
        self._gerenteChaves = gerente

    def getGerente(self):
        return self._gerenteChaves

    def removerGerente(self):
        self._gerenteChaves = ""

    def modificargerente(self, gerente):
        pass

class ChavePrototipo:
    def __init__(self, id = "", nome = '', qr_code = '', posse = 0):
        self._idChave = id
        self._nomeSala = nome
        self._qrCode = qr_code
        self._posse = posse

    def clonar(self, n):
        copia = copy.copy(self)
        return copia

import copy

class Chave(ChavePrototipo):
    def __init__(self, id_chave, nome, qr_code, posse):
        super().__init__(id_chave, nome, qr_code, posse)

    def setId(self, nome):
        self._idChave = nome

    def setNomeSala(self, nome):
        self._nomeSala = nome

    def setQrCode(self, cod):
        self._qrCode = cod

    def setPosse(self, id):
        self._posse = id

    def getId(self):
        return self._idChave

    def getNomeSala(self):
        return self._qrCode

    def getQrCode(self):
        return self._qrCode

    def getPosse(self):
        return self._posse


from abc import ABC, abstractmethod
class Usuario(ABC):
    def __init__(self, nome, senha, email):
        self._nome = nome
        self._email = email
        self._senha = senha

    def setNome(self, nome):
        self._nome = nome

    def setEmail(self, email):
        self._email = email

    def setSenha(self, senha):
        self._senha = senha

    def getNome(self):
        return self._nome

    def getEmail(self):
        return self._email

    def getSenha(self):
        return self._senha


    @abstractmethod
    def pegarChave(self, chave):
        pass

    #@abstractmethod
    #def passarChaveAluno(self, chave, aluno):
        #pass

    @abstractmethod
    def passarChave(self, funcionario):
        pass


class Funcionario(Usuario): #falta implementar
    def __init__(self, nome, senha, email, contrato):
        super().__init__(nome, senha, email)
        self._contrato = contrato

    def setContrato(self, tipo):
        self._contrato = tipo

    def getContrato(self):
        return self._contrato

    def pegarChave(self, chave, id_user):
        table = supabase.table("chaves").select('id', 'nomeSala', 'qrCode', 'posse').eq("id", chave.getId()).execute()
        print(table.data)
        if table.data != []:
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

class Professor(Funcionario):
    def __init__(self, nome, senha, email, contrato, matricula):
        super().__init__(nome, senha, email, contrato)
        self._matricula = matricula

    def setMatricula(self, matricula):
        self._matricula = matricula

    def getMatricula(self):
        return self._matricula

    def consultarChaveAluno(self, aluno):
        # Consulta a tabela alunos_chaves a procura das chaves que o aluno tem permissão(obs: daquele professor)
        pass

    def concederPermissao(self, aluno, chave):
        # adiciona permissao
        pass

    def revogarPermissao(self, aluno, chave):
        # deleta a permissao
        pass


class Gerente(Funcionario):
    def __init__(self, nome="", senha="", email="", contrato="", id=""):
        super().__init__(nome, senha, email, contrato)
        self._id = id

    def setId(self, num):
        self._id = num

    def gerarQrCode(self, gerador):
        pass

    def cadastrarChave(self, id, nome, cod_qr):
        # adicionar na tabela chaves e na instancia de Sistema
        pass

    def modificarChave(self, chave):
        # modificar na tabela chaves e na instancia de sistema

        pass

    def removerChave(self, chave):
        # delete na ocorrencia da tabela chaves e na instancia de sistema
        pass

    def AcessarChavesCadastradas(self, gerenciador):
        return gerenciador.acessarChaves()

    def adicionarUsuario(self, usuario):
        # adcionar na tabela usuarios e na instancia de sistema
        pass

    def modificarUsuario(self, usuario):
        # modificar a tabela usuarios e o objeto usuario
        pass

    def removerUsuario(self, usuario):
        # delete em ocorrencia na tabela usuarios
        pass

import qrcode
@app.route("/gerarQRCode/<cod>/<name>", methods = ["GET", "POST"])
class geradorQRCode():
#     def __init__(self, cod):
#         self.codigo = cod
#
    def __init__(self):
            pass

    def setCodigo(self, cod):
      self.codigo = cod

    def getCod(self):
      return self.codigo

    def gerarQRCode(self, cod, name):
      img = qrcode.make(cod)
      img = qrcode.make(cod)
      img_path = name + ".jpg"
      img.save(img_path)
      return img_path
      if os.path.exists(img_path):
         return f"QR Code gerado com sucesso e salvo em {img_path}"
      else:
         return "Falha ao gerar o QR Code"

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
        self._listChaves.append(chave)

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

##Adicionei da branch de jeremias

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