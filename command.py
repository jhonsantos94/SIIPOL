# command.py
from abc import ABC, abstractmethod
from usuario_service import UsuarioService

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class RegisterUserCommand(Command):
    def __init__(self, admin_username, admin_password, new_username, new_password, role):
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.new_username = new_username
        self.new_password = new_password
        self.role = role

    def execute(self):
        return UsuarioService.registrar_usuario(self.admin_username, self.admin_password, self.new_username, self.new_password, self.role)

class LoginUserCommand(Command):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def execute(self):
        return UsuarioService.autenticar_usuario(self.username, self.password)
