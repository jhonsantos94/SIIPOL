# main.py
import tkinter as tk
from tkinter import ttk
from facade import SIIPOLFacade
from database import crear_base_datos

def ventana_admin():
    ventana = tk.Tk()
    ventana.title("Panel de Administrador")

    tk.Label(ventana, text="Usuarios registrados").pack()

    tree = ttk.Treeview(ventana)
    tree["columns"] = ("1", "2", "3")
    tree.column("#0", width=50)
    tree.column("1", width=100)
    tree.column("2", width=500)
    tree.column("3", width=200)
    tree.heading("#0", text="ID")
    tree.heading("1", text="Usuario")
    tree.heading("2", text="Contraseña")
    tree.heading("3", text="Rol")
    tree.pack()

    # Obtener los usuarios de la base de datos
    usuarios = SIIPOLFacade.obtener_usuarios()

    # Insertar los usuarios en el treeview con las contraseñas encriptadas
    for usuario in usuarios:
        password_encriptada = SIIPOLFacade.encriptar_password(usuario[2])
        tree.insert("", "end", text=usuario[0], values=(usuario[1], password_encriptada, usuario[3]))

    ventana.mainloop()

def ventana_usuario(usuario):
    ventana = tk.Tk()
    ventana.title(f"Panel de Usuario - {usuario.get_role()}")

    tk.Label(ventana, text=f"Bienvenido {usuario.get_role()}").pack()
    # Aquí se pueden agregar más funcionalidades específicas para los usuarios técnicos o investigadores

    ventana.mainloop()

def ventana_login():
    ventana_login = tk.Tk()
    ventana_login.title("SISTEMA INTEGRADO DE INFORMACION DE BASE DE DATOS")

    tk.Label(ventana_login, text="Usuario").grid(row=0, column=0)
    tk.Label(ventana_login, text="Contraseña").grid(row=1, column=0)

    entry_username = tk.Entry(ventana_login)
    entry_password = tk.Entry(ventana_login, show="*")

    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    tk.Button(ventana_login, text="Login", command=lambda: SIIPOLFacade.login(entry_username, entry_password, ventana_login, ventana_admin, ventana_usuario)).grid(row=2, column=0, columnspan=2)
    tk.Button(ventana_login, text="Registrar", command=lambda: ventana_registro(ventana_login)).grid(row=3, column=0, columnspan=2)

    return ventana_login

def ventana_registro(ventana_login):
    ventana_login.destroy()

    ventana_registro = tk.Tk()
    ventana_registro.title("Registro")

    tk.Label(ventana_registro, text="Admin Usuario").grid(row=0, column=0)
    tk.Label(ventana_registro, text="Admin Contraseña").grid(row=1, column=0)
    tk.Label(ventana_registro, text="Nuevo Usuario").grid(row=2, column=0)
    tk.Label(ventana_registro, text="Nueva Contraseña").grid(row=3, column=0)
    tk.Label(ventana_registro, text="Rol").grid(row=4, column=0)

    entry_admin_username = tk.Entry(ventana_registro)
    entry_admin_password = tk.Entry(ventana_registro, show="*")
    entry_new_username = tk.Entry(ventana_registro)
    entry_new_password = tk.Entry(ventana_registro, show="*")
    role_var = tk.StringVar(ventana_registro)
    role_var.set("TecnicoForense")

    entry_admin_username.grid(row=0, column=1)
    entry_admin_password.grid(row=1, column=1)
    entry_new_username.grid(row=2, column=1)
    entry_new_password.grid(row=3, column=1)
    tk.OptionMenu(ventana_registro, role_var, "TecnicoForense", "InvestigadorCriminalistico").grid(row=4, column=1)

    tk.Button(ventana_registro, text="Registrar", command=lambda: SIIPOLFacade.register(
        entry_admin_username.get(),
        entry_admin_password.get(),
        entry_new_username.get(),
        entry_new_password.get(),
        role_var.get()
    )).grid(row=5, column=0, columnspan=2)

    ventana_registro.mainloop()

# Ejecutar el programa
crear_base_datos()
ventana_login = ventana_login()
ventana_login.mainloop()