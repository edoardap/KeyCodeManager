from Models.Funcionario import Funcionario
from Models.Usuario import Usuario

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

