from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, id, username, password):
        self.id = id  # Agregar el atributo id
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
    def crear_usuario(id, role, username, password):
        if role == "Administrador":
            return Administrador(id, username, password)
        elif role == "TecnicoForense":
            return TecnicoForense(id, username, password)
        elif role == "InvestigadorCriminalistico":
            return InvestigadorCriminalistico(id, username, password)
        else:
            raise ValueError(f"Rol desconocido: {role}")
