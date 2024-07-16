# facade.py
from tkinter import messagebox
from usuario_service import UsuarioService
from usuario import FabricaUsuario

class SIIPOLFacade:
    @staticmethod
    def login(entry_username, entry_password, ventana_login, ventana_admin, ventana_usuario):
        username = entry_username.get()
        password = entry_password.get()

        usuario = UsuarioService.autenticar_usuario(username, password)
        if usuario:
            messagebox.showinfo("Login exitoso", f"Bienvenido {usuario.username}")
            ventana_login.destroy()
            if usuario.get_role() == 'Administrador':
                ventana_admin()
            else:
                ventana_usuario(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    @staticmethod
    def register(admin_username, admin_password, new_username, new_password, role):
        if UsuarioService.registrar_usuario(admin_username, admin_password, new_username, new_password, role):
            messagebox.showinfo("Registro exitoso", f"Usuario {new_username} creado exitosamente")
        else:
            messagebox.showerror("Error", "Error al registrar el usuario")

    @staticmethod
    def obtener_usuarios():
        return UsuarioService.obtener_usuarios()

    @staticmethod
    def encriptar_password(password):
        return UsuarioService.encriptar_password(password)