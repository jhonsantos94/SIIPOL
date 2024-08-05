import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Asegúrate de importar PIL
from facade import SIIPOLFacade
from database import crear_base_datos
import datetime as dt
import sqlite3
from fpdf import FPDF
import random
import datetime

def ventana_admin():
    ventana = tk.Tk()
    ventana.title("Panel de Administrador")
    ventana.geometry("900x300")
    ventana.iconbitmap("imagenes/logo_SIIPOL.ico")

    # Crear un marco para la barra superior
    top_frame = tk.Frame(ventana)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()
    fecha_formateada = fecha_actual.strftime("%A, %d de %B de %Y")  # Formato: Día, Número de mes, Mes, Año

    # Etiqueta para mostrar la fecha
    fecha_label = tk.Label(top_frame, text=fecha_formateada, font=("Arial", 10))
    fecha_label.pack(side=tk.LEFT, padx=10, pady=10)  # Coloca la etiqueta en la esquina superior izquierda

    # Botón de Cerrar Sesión
    def cerrar_sesion():
        ventana.destroy()  # Cierra la ventana del administrador
        ventana_login = crear_ventana_login()  # Muestra la ventana de inicio de sesión
        ventana_login.mainloop()

    cerrar_sesion_button = tk.Button(top_frame, text="Cerrar Sesión", command=cerrar_sesion)
    cerrar_sesion_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Coloca el botón en la esquina superior derecha

    tk.Label(ventana,font=("Arial", 20), text="Usuarios registrados").pack()

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

def ventana_usuario(usuario, role):
    ventana = tk.Tk()
    ventana.geometry("800x500")
    if role == "TecnicoForense":
        ventana.title("Panel de Técnico Forense")
        ventana.iconbitmap("imagenes/logo_SIIPOL.ico")
        # Crear un marco para la barra superior
        top_frame = tk.Frame(ventana)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()
        fecha_formateada = fecha_actual.strftime("%A, %d de %B de %Y")  # Formato: Día, Número de mes, Mes, Año

        # Etiqueta para mostrar la fecha
        fecha_label = tk.Label(top_frame, text=fecha_formateada, font=("Arial", 10))
        fecha_label.pack(side=tk.LEFT, padx=10, pady=10)  # Coloca la etiqueta en la esquina superior izquierda

        # Botón de Cerrar Sesión
        def cerrar_sesion():
            ventana.destroy()  # Cierra la ventana del administrador
            ventana_login = crear_ventana_login()  # Muestra la ventana de inicio de sesión
            ventana_login.mainloop()

        cerrar_sesion_button = tk.Button(top_frame, text="Cerrar Sesión", command=cerrar_sesion)
        cerrar_sesion_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Coloca el botón en la esquina superior derecha
        # Sección: Recolección de Pruebas
        tk.Label(ventana, text="Recolección de Pruebas", font=("Arial", 16)).pack(pady=10)

        def registrar_nueva_prueba():
            form_window = tk.Toplevel(ventana)
            form_window.title("Registrar Nueva Prueba")

            tk.Label(form_window, text="Tipo de prueba").grid(row=0, column=0, padx=10, pady=5)
            tipo_prueba = ttk.Combobox(form_window, values=["Fibras", "Cabellos", "Tejidos", "Armas", "Sustancias Químicas"])
            tipo_prueba.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Ubicación en la escena").grid(row=1, column=0, padx=10, pady=5)
            ubicacion = tk.Entry(form_window)
            ubicacion.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Método de recolección").grid(row=2, column=0, padx=10, pady=5)
            metodo = tk.Entry(form_window)
            metodo.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Fecha y hora").grid(row=3, column=0, padx=10, pady=5)
            fecha_hora = tk.Entry(form_window)
            fecha_hora.insert(0, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
            fecha_hora.grid(row=3, column=1, padx=10, pady=5)

            def guardar_prueba():
                tipo = tipo_prueba.get()
                ubicacion_texto = ubicacion.get()
                metodo_texto = metodo.get()
                fecha_hora_texto = fecha_hora.get()
                usuario_id = usuario.id  # Asegúrate de que el ID esté disponible

                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO pruebas (tipo, ubicacion, metodo, fecha_hora, usuario_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (tipo, ubicacion_texto, metodo_texto, fecha_hora_texto, usuario_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Prueba registrada")
                form_window.destroy()

            tk.Button(form_window, text="Guardar", command=guardar_prueba).grid(row=4, columnspan=2, pady=10)

        tk.Button(ventana, text="Registrar Nueva Prueba", command=registrar_nueva_prueba).pack(pady=5)

        def ver_historial_pruebas():
            pruebas_window = tk.Toplevel(ventana)
            pruebas_window.title("Historial de Pruebas")
            pruebas_window.geometry("600x400")
            pruebas_window.iconbitmap("imagenes/logo_SIIPOL.ico")

            tree = ttk.Treeview(pruebas_window)
            tree["columns"] = ("1", "2", "3", "4")
            tree.column("#0", width=50)
            tree.column("1", width=150)
            tree.column("2", width=150)
            tree.column("3", width=150)
            tree.column("4", width=100)
            tree.heading("#0", text="ID")
            tree.heading("1", text="Tipo")
            tree.heading("2", text="Ubicación")
            tree.heading("3", text="Método")
            tree.heading("4", text="Fecha y Hora")
            tree.pack(pady=10)

            # Obtener las pruebas de la base de datos
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pruebas")
            pruebas = cursor.fetchall()
            conn.close()

            # Insertar las pruebas en el treeview
            for prueba in pruebas:
                tree.insert("", "end", text=prueba[0], values=(prueba[1], prueba[2], prueba[3], prueba[4]))

        tk.Button(ventana, text="Ver Historial de Pruebas", command=ver_historial_pruebas).pack(pady=5)

        # Sección: Análisis de Pruebas
        tk.Label(ventana, text="Análisis de Pruebas", font=("Arial", 16)).pack(pady=10)

        def ver_resultados_analisis():
            resultado_aleatorio = random.choice(["Análisis ejecutado con éxito, descargue el informe", "Informe fallido, repita el proceso"])
            messagebox.showinfo("Resultados de Análisis", resultado_aleatorio)

        tk.Button(ventana, text="Iniciar Análisis", command=lambda: messagebox.showinfo("Análisis", "Iniciando análisis")).pack(pady=5)
        tk.Button(ventana, text="Ver Resultados de Análisis", command=ver_resultados_analisis).pack(pady=5)

        # Sección: Documentación
        tk.Label(ventana, text="Documentación", font=("Arial", 16)).pack(pady=10)

        def agregar_documentacion():
            form_window = tk.Toplevel(ventana)
            form_window.title("Agregar Documentación")
            form_window.iconbitmap("imagenes/logo_SIIPOL.ico")
            tk.Label(form_window, text="Fecha").grid(row=0, column=0, padx=10, pady=5)
            fecha = tk.Entry(form_window)
            fecha.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Lugar").grid(row=1, column=0, padx=10, pady=5)
            lugar = tk.Entry(form_window)
            lugar.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Caso Número").grid(row=2, column=0, padx=10, pady=5)
            caso_numero = tk.Entry(form_window)
            caso_numero.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Acusado").grid(row=3, column=0, padx=10, pady=5)
            acusado = tk.Entry(form_window)
            acusado.grid(row=3, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Víctima").grid(row=4, column=0, padx=10, pady=5)
            victima = tk.Entry(form_window)
            victima.grid(row=4, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Delito").grid(row=5, column=0, padx=10, pady=5)
            delito = tk.Entry(form_window)
            delito.grid(row=5, column=1, padx=10, pady=5)

            def guardar_documentacion():
                fecha_texto = fecha.get()
                lugar_texto = lugar.get()
                caso_numero_texto = caso_numero.get()
                acusado_texto = acusado.get()
                victima_texto = victima.get()
                delito_texto = delito.get()
                usuario_id = usuario.id  # Asegúrate de que el ID esté disponible

                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO documentacion (fecha, lugar, caso_numero, acusado, victima, delito, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (fecha_texto, lugar_texto, caso_numero_texto, acusado_texto, victima_texto, delito_texto, usuario_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Documentación agregada")
                form_window.destroy()

            tk.Button(form_window, text="Guardar", command=guardar_documentacion).grid(row=6, columnspan=2, pady=10)

        tk.Button(ventana, text="Agregar Documentación", command=agregar_documentacion).pack(pady=5)

        def generar_informe_caso():
            informe_window = tk.Toplevel(ventana)
            informe_window.title("Generar Informe de Caso")
            informe_window.geometry("600x400")
            informe_window.iconbitmap("imagenes/logo_SIIPOL.ico")
            tree = ttk.Treeview(informe_window)
            tree["columns"] = ("1", "2", "3", "4", "5", "6")
            tree.column("#0", width=50)
            tree.column("1", width=100)
            tree.column("2", width=100)
            tree.column("3", width=100)
            tree.column("4", width=100)
            tree.column("5", width=100)
            tree.column("6", width=100)
            tree.heading("#0", text="ID")
            tree.heading("1", text="Fecha")
            tree.heading("2", text="Lugar")
            tree.heading("3", text="Caso Número")
            tree.heading("4", text="Acusado")
            tree.heading("5", text="Víctima")
            tree.heading("6", text="Delito")
            tree.pack(pady=10)

            # Obtener la documentación de la base de datos
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documentacion")
            documentacion = cursor.fetchall()
            conn.close()

            # Insertar la documentación en el treeview
            for doc in documentacion:
                tree.insert("", "end", text=doc[0], values=(doc[1], doc[2], doc[3], doc[4], doc[5], doc[6]))

            def generar_pdf():
                selected_item = tree.focus()
                if selected_item:
                    item_data = tree.item(selected_item)
                    fecha = item_data["values"][0]
                    lugar = item_data["values"][1]
                    caso_numero = item_data["values"][2]
                    acusado = item_data["values"][3]
                    victima = item_data["values"][4]
                    delito = item_data["values"][5]

                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)

                    pdf.cell(200, 10, txt="Informe de Caso", ln=True, align='C')
                    pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
                    pdf.cell(200, 10, txt=f"Lugar: {lugar}", ln=True)
                    pdf.cell(200, 10, txt=f"Caso Número: {caso_numero}", ln=True)
                    pdf.cell(200, 10, txt=f"Acusado: {acusado}", ln=True)
                    pdf.cell(200, 10, txt=f"Víctima: {victima}", ln=True)
                    pdf.cell(200, 10, txt=f"Delito: {delito}", ln=True)

                    pdf_file_name = "informe_caso.pdf"
                    pdf.output(pdf_file_name)

                    messagebox.showinfo("Éxito", f"Informe generado: {pdf_file_name}")

            tk.Button(informe_window, text="Generar Informe", command=generar_pdf).pack(pady=20)

        tk.Button(ventana, text="Generar Informe de Caso", command=generar_informe_caso).pack(pady=5)

        # Sección: Testimonio
        tk.Label(ventana, text="Testimonio", font=("Arial", 16)).pack(pady=10)

        tk.Button(ventana, text="Preparar Testimonio", command=lambda: messagebox.showinfo("Testimonio", "Preparando testimonio")).pack(pady=5)

    elif role == "InvestigadorCriminalistico":
        ventana.title("Panel de Investigador Criminalístico")
        ventana.iconbitmap("imagenes/logo_SIIPOL.ico")
        
        # Crear un marco para la barra superior
    top_frame = tk.Frame(ventana)
    top_frame.pack(side=tk.TOP, fill=tk.X)

        # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()
    fecha_formateada = fecha_actual.strftime("%A, %d de %B de %Y")  # Formato: Día, Número de mes, Mes, Año

        # Etiqueta para mostrar la fecha
    fecha_label = tk.Label(top_frame, text=fecha_formateada, font=("Arial", 10))
    fecha_label.pack(side=tk.LEFT, padx=10, pady=10)  # Coloca la etiqueta en la esquina superior izquierda

        # Botón de Cerrar Sesión
    def cerrar_sesion():
            ventana.destroy()  # Cierra la ventana del administrador
            ventana_login = crear_ventana_login()  # Muestra la ventana de inicio de sesión
            ventana_login.mainloop()

    cerrar_sesion_button = tk.Button(top_frame, text="Cerrar Sesión", command=cerrar_sesion)
    cerrar_sesion_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Coloca el botón en la esquina superior derecha
        # Sección: Investigación de Escena del Crimen
    tk.Label(ventana, text="Investigación de Escena del Crimen", font=("Arial", 16)).pack(pady=10)
    # Botón de Cerrar Sesión
    def cerrar_sesion():
            ventana.destroy()  # Cierra la ventana 
            crear_ventana_login()  # Muestra la ventana de inicio de sesión

            cerrar_sesion_button = tk.Button(ventana, text="Cerrar Sesión", command=cerrar_sesion)
            cerrar_sesion_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)  # Coloca el botón en la esquina superior derecha
            
    def registrar_escena():
            form_window = tk.Toplevel(ventana)
            form_window.title("Registrar Escena del Crimen")
            form_window.iconbitmap("imagenes/logo_SIIPOL.ico")
            tk.Label(form_window, text="Descripción de la escena").grid(row=0, column=0, padx=10, pady=5)
            descripcion = tk.Entry(form_window)
            descripcion.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Fecha y hora").grid(row=1, column=0, padx=10, pady=5)
            fecha_hora = tk.Entry(form_window)
            fecha_hora.insert(0, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
            fecha_hora.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Ubicación").grid(row=2, column=0, padx=10, pady=5)
            ubicacion = tk.Entry(form_window)
            ubicacion.grid(row=2, column=1, padx=10, pady=5)

            def guardar_escena():
                descripcion_texto = descripcion.get()
                fecha_hora_texto = fecha_hora.get()
                ubicacion_texto = ubicacion.get()
                usuario_id = usuario.id  # Asegúrate de que el ID esté disponible

                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO escenas (descripcion, fecha_hora, ubicacion, usuario_id)
                    VALUES (?, ?, ?, ?)
                ''', (descripcion_texto, fecha_hora_texto, ubicacion_texto, usuario_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Escena registrada")
                form_window.destroy()

            tk.Button(form_window, text="Guardar", command=guardar_escena).grid(row=3, columnspan=2, pady=10)

    tk.Button(ventana, text="Registrar Escena del Crimen", command=registrar_escena).pack(pady=5)

    def ver_escenas_registradas():
            escenas_window = tk.Toplevel(ventana)
            escenas_window.title("Escenas Registradas")
            escenas_window.geometry("600x400")
            escenas_window.iconbitmap("imagenes/logo_SIIPOL.ico")
            tree = ttk.Treeview(escenas_window)
            tree["columns"] = ("1", "2", "3")
            tree.column("#0", width=50)
            tree.column("1", width=200)
            tree.column("2", width=200)
            tree.column("3", width=100)
            tree.heading("#0", text="ID")
            tree.heading("1", text="Descripción")
            tree.heading("2", text="Fecha y Hora")
            tree.heading("3", text="Ubicación")
            tree.pack(pady=10)

            # Obtener las escenas de la base de datos
            escenas = SIIPOLFacade.obtener_escenas()

            # Insertar las escenas en el treeview
            for escena in escenas:
                tree.insert("", "end", text=escena[0], values=(escena[1], escena[2], escena[3]))

    tk.Button(ventana, text="Ver Escenas Registradas", command=ver_escenas_registradas).pack(pady=5)

        # Sección: Entrevistas
    tk.Label(ventana, text="Entrevistas", font=("Arial", 16)).pack(pady=10)

    def registrar_entrevista():
            form_window = tk.Toplevel(ventana)
            form_window.title("Registrar Entrevista")
            form_window.iconbitmap("imagenes/logo_SIIPOL.ico")
            tk.Label(form_window, text="Nombre del testigo/sospechoso").grid(row=0, column=0, padx=10, pady=5)
            nombre = tk.Entry(form_window)
            nombre.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Resumen de la entrevista").grid(row=1, column=0, padx=10, pady=5)
            resumen = tk.Entry(form_window)
            resumen.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Fecha y hora").grid(row=2, column=0, padx=10, pady=5)
            fecha_hora = tk.Entry(form_window)
            fecha_hora.insert(0, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
            fecha_hora.grid(row=2, column=1, padx=10, pady=5)

            def guardar_entrevista():
                nombre_texto = nombre.get()
                resumen_texto = resumen.get()
                fecha_hora_texto = fecha_hora.get()
                usuario_id = usuario.id  # Asegúrate de que el ID esté disponible

                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO entrevistas (nombre, resumen, fecha_hora, usuario_id)
                    VALUES (?, ?, ?, ?)
                ''', (nombre_texto, resumen_texto, fecha_hora_texto, usuario_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Entrevista registrada")
                form_window.destroy()

            tk.Button(form_window, text="Guardar", command=guardar_entrevista).grid(row=3, columnspan=2, pady=10)

    tk.Button(ventana, text="Registrar Entrevista", command=registrar_entrevista).pack(pady=5)

    def ver_entrevistas_registradas():
            entrevistas_window = tk.Toplevel(ventana)
            entrevistas_window.title("Entrevistas Registradas")
            entrevistas_window.geometry("600x400")
            entrevistas_window.iconbitmap("imagenes/logo_SIIPOL.ico")

            tree = ttk.Treeview(entrevistas_window)
            tree["columns"] = ("1", "2", "3")
            tree.column("#0", width=50)
            tree.column("1", width=200)
            tree.column("2", width=200)
            tree.column("3", width=100)
            tree.heading("#0", text="ID")
            tree.heading("1", text="Nombre")
            tree.heading("2", text="Resumen")
            tree.heading("3", text="Fecha y Hora")
            tree.pack(pady=10)

            # Obtener las entrevistas de la base de datos
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM entrevistas")
            entrevistas = cursor.fetchall()
            conn.close()

            # Insertar las entrevistas en el treeview
            for entrevista in entrevistas:
                tree.insert("", "end", text=entrevista[0], values=(entrevista[1], entrevista[2], entrevista[3]))

    tk.Button(ventana, text="Ver Historial de Entrevistas", command=ver_entrevistas_registradas).pack(pady=5)

        # Sección: Análisis de Evidencias
    tk.Label(ventana, text="Análisis de Evidencias", font=("Arial", 16)).pack(pady=10)

    def agregar_evidencia():
            form_window = tk.Toplevel(ventana)
            form_window.title("Agregar Evidencia")

            tk.Label(form_window, text="Descripción de la evidencia").grid(row=0, column=0, padx=10, pady=5)
            descripcion = tk.Entry(form_window)
            descripcion.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form_window, text="Fecha y hora").grid(row=1, column=0, padx=10, pady=5)
            fecha_hora = tk.Entry(form_window)
            fecha_hora.insert(0, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
            fecha_hora.grid(row=1, column=1, padx=10, pady=5)

            def guardar_evidencia():
                descripcion_texto = descripcion.get()
                fecha_hora_texto = fecha_hora.get()
                usuario_id = usuario.id  # Asegúrate de que el ID esté disponible

                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO evidencias (descripcion, fecha_hora, usuario_id)
                    VALUES (?, ?, ?)
                ''', (descripcion_texto, fecha_hora_texto, usuario_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Evidencia registrada")
                form_window.destroy()

            tk.Button(form_window, text="Guardar", command=guardar_evidencia).grid(row=2, columnspan=2, pady=10)

    tk.Button(ventana, text="Agregar Evidencia", command=agregar_evidencia).pack(pady=5)

    def ver_evidencias_registradas():
            evidencias_window = tk.Toplevel(ventana)
            evidencias_window.title("Evidencias Registradas")
            evidencias_window.geometry("600x400")

            tree = ttk.Treeview(evidencias_window)
            tree["columns"] = ("1", "2")
            tree.column("#0", width=50)
            tree.column("1", width=200)
            tree.column("2", width=200)
            tree.heading("#0", text="ID")
            tree.heading("1", text="Descripción")
            tree.heading("2", text="Fecha y Hora")
            tree.pack(pady=10)

            # Obtener las evidencias de la base de datos
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM evidencias")
            evidencias = cursor.fetchall()
            conn.close()

            # Insertar las evidencias en el treeview
            for evidencia in evidencias:
                tree.insert("", "end", text=evidencia[0], values=(evidencia[1], evidencia[2]))

    tk.Button(ventana, text="Ver Evidencias Analizadas", command=ver_evidencias_registradas).pack(pady=5)

        # Sección: Generar Informe
    tk.Label(ventana, text="Generar Informe", font=("Arial", 16)).pack(pady=10)

    def generar_informe_caso():
            informe_window = tk.Toplevel(ventana)
            informe_window.title("Generar Informe de Caso")
            informe_window.geometry("600x400")

            tree = ttk.Treeview(informe_window)
            tree["columns"] = ("1", "2", "3", "4", "5", "6")
            tree.column("#0", width=50)
            tree.column("1", width=100)
            tree.column("2", width=100)
            tree.column("3", width=100)
            tree.column("4", width=100)
            tree.column("5", width=100)
            tree.column("6", width=100)
            tree.heading("#0", text="ID")
            tree.heading("1", text="Fecha")
            tree.heading("2", text="Lugar")
            tree.heading("3", text="Caso Número")
            tree.heading("4", text="Acusado")
            tree.heading("5", text="Víctima")
            tree.heading("6", text="Delito")
            tree.pack(pady=10)

            # Obtener la documentación de la base de datos
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documentacion")
            documentacion = cursor.fetchall()
            conn.close()

            # Insertar la documentación en el treeview
            for doc in documentacion:
                tree.insert("", "end", text=doc[0], values=(doc[1], doc[2], doc[3], doc[4], doc[5], doc[6]))

            def generar_pdf():
                selected_item = tree.focus()
                if selected_item:
                    item_data = tree.item(selected_item)
                    fecha = item_data["values"][0]
                    lugar = item_data["values"][1]
                    caso_numero = item_data["values"][2]
                    acusado = item_data["values"][3]
                    victima = item_data["values"][4]
                    delito = item_data["values"][5]

                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)

                    pdf.cell(200, 10, txt="Informe de Caso", ln=True, align='C')
                    pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
                    pdf.cell(200, 10, txt=f"Lugar: {lugar}", ln=True)
                    pdf.cell(200, 10, txt=f"Caso Número: {caso_numero}", ln=True)
                    pdf.cell(200, 10, txt=f"Acusado: {acusado}", ln=True)
                    pdf.cell(200, 10, txt=f"Víctima: {victima}", ln=True)
                    pdf.cell(200, 10, txt=f"Delito: {delito}", ln=True)

                    pdf_file_name = "informe_caso.pdf"
                    pdf.output(pdf_file_name)

                    messagebox.showinfo("Éxito", f"Informe generado: {pdf_file_name}")

            tk.Button(informe_window, text="Generar Informe", command=generar_pdf).pack(pady=20)

    tk.Button(ventana, text="Generar Informe de Caso", command=generar_informe_caso).pack(pady=5)

        # Sección: Testimonio
    tk.Label(ventana, text="Testimonio", font=("Arial", 16)).pack(pady=10)

    tk.Button(ventana, text="Preparar Testimonio", command=lambda: messagebox.showinfo("Testimonio", "Preparando testimonio")).pack(pady=5)

    ventana.mainloop()

def crear_ventana_login():
    ventana_login = tk.Tk()
    ventana_login.title("SISTEMA INTEGRADO DE INFORMACION DE BASE DE DATOS")
    ventana_login.geometry("400x500")
    ventana_login.iconbitmap("imagenes/logo_SIIPOL.ico")
    # Crear un marco para contener el contenido
    content_frame = tk.Frame(ventana_login)
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Cargar y mostrar la imagen
    try:
        imagen = Image.open(r"imagenes/logo_SIIPOL.png")  # Cambia esto a la ruta de tu imagen
        imagen = imagen.resize((100, 100), Image.LANCZOS)  # Usa Image.LANCZOS en lugar de Image.ANTIALIAS
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(content_frame, image=imagen_tk)
        label_imagen.image = imagen_tk  # Mantener una referencia a la imagen
        label_imagen.grid(row=0, column=0, columnspan=2, pady=10)  # Colocar la imagen en la fila 0
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    # Crear etiquetas y entradas dentro del marco
    tk.Label(content_frame, text="Usuario").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(content_frame, text="Contraseña").grid(row=2, column=0, padx=20, pady=5, sticky="e")

    entry_username = tk.Entry(content_frame)
    entry_password = tk.Entry(content_frame, show="*")

    entry_username.grid(row=1, column=1, padx=20, pady=20)
    entry_password.grid(row=2, column=1, padx=20, pady=20)

    tk.Button(content_frame, text="Login", command=lambda: SIIPOLFacade.login(
        entry_username, 
        entry_password, 
        ventana_login, 
        ventana_admin, 
        ventana_usuario
    )).grid(row=3, column=0, columnspan=2, pady=10)
    
    tk.Button(content_frame, text="Registrar", command=lambda: ventana_registro(ventana_login)).grid(row=4, column=0, columnspan=2, pady=10)

    return ventana_login

def ventana_registro(ventana_login):
    ventana_login.destroy()
   
    ventana_registro = tk.Tk()
    ventana_registro.title("Registro")
    ventana_registro.geometry("600x300")

    # Botón de Cerrar Sesión
    def cerrar_sesion():
        ventana_registro.destroy()  # Cierra la ventana de registro
        ventana_login = crear_ventana_login()  # Muestra la ventana de inicio de sesión
        ventana_login.mainloop()

    cerrar_sesion_button = tk.Button(ventana_registro, text="Iniciar Sesión", command=cerrar_sesion)
    cerrar_sesion_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)  # Coloca el botón en la esquina superior derecha

    # Crear un marco para contener el contenido
    content_frame = tk.Frame(ventana_registro)
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Crear etiquetas y entradas dentro del marco
    tk.Label(content_frame, text="Admin Usuario").grid(row=0, column=0, padx=20, pady=10, sticky="e")
    tk.Label(content_frame, text="Admin Contraseña").grid(row=1, column=0, padx=20, pady=10, sticky="e")
    tk.Label(content_frame, text="Nuevo Usuario").grid(row=2, column=0, padx=20, pady=10, sticky="e")
    tk.Label(content_frame, text="Nueva Contraseña").grid(row=3, column=0, padx=20, pady=10, sticky="e")
    tk.Label(content_frame, text="Rol").grid(row=4, column=0, padx=20, pady=10, sticky="e")

    entry_admin_username = tk.Entry(content_frame)
    entry_admin_password = tk.Entry(content_frame, show="*")
    entry_new_username = tk.Entry(content_frame)
    entry_new_password = tk.Entry(content_frame, show="*")
    role_var = tk.StringVar(content_frame)
    role_var.set("TecnicoForense")

    entry_admin_username.grid(row=0, column=1, padx=20, pady=10)
    entry_admin_password.grid(row=1, column=1, padx=20, pady=10)
    entry_new_username.grid(row=2, column=1, padx=20, pady=10)
    entry_new_password.grid(row=3, column=1, padx=20, pady=10)
    tk.OptionMenu(content_frame, role_var, "TecnicoForense", "InvestigadorCriminalistico").grid(row=4, column=1, padx=20, pady=10)

    tk.Button(content_frame, text="Registrar", command=lambda: SIIPOLFacade.register(
        entry_admin_username.get(),
        entry_admin_password.get(),
        entry_new_username.get(),
        entry_new_password.get(),
        role_var.get()
    )).grid(row=5, column=0, columnspan=2, pady=20)

    ventana_registro.mainloop()

# Ejecutar el programa
crear_base_datos()
ventana_login = crear_ventana_login()
ventana_login.mainloop()
