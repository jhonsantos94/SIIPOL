# usuario.py
from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abstractmethod
    def get_role(self):
        pass

class Administrador(Usuario):
    def get_role(self):
        return "Administrador"

class TecnicoForense(Usuario):
    def get_role(self):
        return "TecnicoForense"

class InvestigadorCriminalistico(Usuario):
    def get_role(self):
        return "InvestigadorCriminalistico"

class FabricaUsuario:
    @staticmethod
    def crear_usuario(role, username, password):
        if role == "Administrador":
            return Administrador(username, password)
        elif role == "TecnicoForense":
            return TecnicoForense(username, password)
        elif role == "InvestigadorCriminalistico":
            return InvestigadorCriminalistico(username, password)
        else:
            raise ValueError(f"Rol desconocido: {role}")