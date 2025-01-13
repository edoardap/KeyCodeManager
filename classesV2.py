from supabase import create_client
from abc import ABC, abstractmethod
import os

class Proxy():
    def __init__(self, token):
        self.token = token

    def conferirAcesso(self):
        pass

    def operacao(self):
        pass

class Observer(ABC):
    @abstractmethod
    def adaptar(self):
        pass

class ObserverChave(Observer):
    def adaptar(self):
        "implementacao"
        pass

