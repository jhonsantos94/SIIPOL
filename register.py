import hashlib
import sqlite3
from tkinter import messagebox
from usuario import FabricaUsuario
from facade import SIIPOLFacade

def register(entry_admin_username, entry_admin_password, entry_new_username, entry_new_password, role_var):
    admin_username = entry_admin_username.get()
    admin_password = entry_admin_password.get()
    new_username = entry_new_username.get()
    new_password = entry_new_password.get()
    role = role_var.get()
    
    SIIPOLFacade.register(admin_username, admin_password, new_username, new_password, role)