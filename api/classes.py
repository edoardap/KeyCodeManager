import threading
class SingletonSistema():
    _instancia = None
    _lock = threading.Lock()

    def __init__(self):
        if SingletonSistema._instancia != None:
            raise Exception("This class is a singleton class!")
        else:
            self._usuarios = []
            self._chaves = []
            self._gerenteChaves = ""
            SingletonSistema._instancia = self

    @staticmethod
    def getInstance():
        with SingletonSistema._lock:
            if SingletonSistema._instancia is None:
                return SingletonSistema()
            return SingletonSistema._instancia

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

    def setGerente(self, gerente):
        self._gerenteChaves = gerente

    def getGerente(self):
        return self._gerenteChaves

    def removerGerente(self):
        self._gerenteChaves = ""

    def modificargerente(self, gerente):
        pass

class ChavePrototipo:
    def __init__(self, id, nome, qr_code):
        self._idChave = id
        self._nomeSala = nome
        self._qrCode = qr_code

    def setId(self, nome):
        self._idChave = nome

    def setNomeSala(self, nome):
        self._nomeSala = nome

    def setQrCode(self, cod):
        self._qrCode = cod

    def getId(self):
        return self._idChave

    def getNomeSala(self):
        return self._qrCode

    def getQrCode(self):
        return self._qrCode

import copy

class chavetemporaria(ChavePrototipo):
    def __init__(self, id_chave, nome, qr_code):
        super().__init__(id_chave, nome, qr_code)

    def clonar(self, n):
        copias_chaves = []
        for i in range(n):
            copia = copy.copy(self)
            copias_chaves.append(copia)
        return copias_chaves

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
    def __init__(self, nome, senha, email, contrato, id, gerador_qr):
        super().__init__(nome, senha, email, contrato)
        self._id = id
        self._geradorQr = gerador_qr

    def setId(self, num):
        self._id = num

    def setGeradorQrCode(self, gerador):
        self._geradorQr = gerador

    def cadastrarChave(self, id, nome, cod_qr):
        # adicionar na tabela chaves e na instancia de Sistema
        pass

    def modificarChave(self, chave):
        # modificar na tabela chaves e na instancia de sistema

        pass

    def removerChave(self, chave):
        # delete na ocorrencia da tabela chaves e na instancia de sistema
        pass

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
