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
    conn.commit()
    
    # Insertar usuario administrador inicial
    cursor.execute("SELECT * FROM usuarios WHERE username='admin'")
    if cursor.fetchone() is None:
        SIIPOLFacade.register('admin', 'admin123', 'admin', 'admin123', 'Administrador')

    conn.close()