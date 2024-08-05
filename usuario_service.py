# usuario_service.py
import hashlib
import sqlite3
from usuario import FabricaUsuario

class UsuarioService:
    @staticmethod
    def autenticar_usuario(username, password):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            if password == user[2]:  # user[2] es la contraseña
                return FabricaUsuario.crear_usuario(user[0], user[3], user[1], user[2])  # user[0] es el id
        return None

    @staticmethod
    def registrar_usuario(admin_username, admin_password, new_username, new_password, role):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
                           (new_username, new_password, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def obtener_usuarios():
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    @staticmethod
    def encriptar_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def obtener_escenas():
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM escenas")
        escenas = cursor.fetchall()
        conn.close()
        return escenas
