import sqlite3
import os

os.makedirs("banco", exist_ok=True)

con = sqlite3.connect("banco/usuarios.db")
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')

con.commit()
con.close()
print("Banco e tabela criados com sucesso.")
