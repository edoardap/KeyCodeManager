from supabase import create_client
from flask import render_template, request
supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

class TelaLogin():
    def __init__(self, email="", senha="", nome=""):
        self.email = email
        self.senha = senha
        self.nome = nome

    def setEmail(self, email):
        self.email = email

    def setSenha(self, password):
        self.senha = password

    def setNome(self, nome):
        self.nome = nome

    def getEmail(self):
        return self.email

    def getSenha(self):
        return self.senha

    def getNome(self):
        return self.nome

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
        self._usuarios.remove(usuario)
        #chamada ao banco

    def alterarUsuario(self, usuario):
        pass

    def cadastrarChave(self, chave):
        self._chaves.append(chave)

    def removerChave(self, chave):
        self._chaves.remove(chave)

    def alterarChave(self):
        pass

    def acessarChaves(self):
        if request.method == "GET":
            return supabase.table('chaves').select('id', 'nomeSala', 'qrCode').execute()


    def setGerente(self, gerente):
        self._gerenteChaves = gerente

    def getGerente(self):
        return self._gerenteChaves

    def removerGerente(self):
        self._gerenteChaves = ""

    def modificargerente(self, gerente):
        pass

class ChavePrototipo:
    def __init__(self, id = 0, nome = '', qr_code = '', posse = 0):
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
    def passarChaveAluno(self, chave, aluno):
        pass

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
class geradorQRCode():
    def __init__(self, cod):
        self.codigo = cod

    def setCodigo(self, cod):
      self.codigo = cod

    def getCod(self):
      return self.codigo

    def gerarQRCode(self, cod, name):
      img = qrcode.make(cod)
      img.save(name + ".jpg")

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


