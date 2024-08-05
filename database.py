import sqlite3
from facade import SIIPOLFacade

def crear_base_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pruebas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            metodo TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrevistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            resumen TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            lugar TEXT NOT NULL,
            caso_numero TEXT NOT NULL,
            acusado TEXT NOT NULL,
            victima TEXT NOT NULL,
            delito TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    
    # Insertar usuario administrador inicial
    cursor.execute("SELECT * FROM usuarios WHERE username='admin'")
    if cursor.fetchone() is None:
        # Asegúrate de que esta línea esté correctamente definida en tu código
        SIIPOLFacade.register('admin', 'admin123', 'admin', 'admin123', 'Administrador')

    conn.close()
