import sqlite3
import psycopg2

# Conexão com o banco de dados SQLite3
sqlite_conn = sqlite3.connect('./Banco/BancoGtech.db')
sqlite_cur = sqlite_conn.cursor()

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="PostgreSQL16",
    user="root",
    password="root",
    
)

cursor = conn.cursor()


# Seleciona todos os dados da tabela no SQLite
sqlite_cur.execute("SELECT * FROM TB_CLIENTE")
dados_sqlite = sqlite_cur.fetchall()
print(dados_sqlite)


for row in dados_sqlite:
    cursor.execute("""
        INSERT INTO TB_CLIENTE (ID_CLIENTE, NOME, TELEFONE, DATA_CADASTRO)
        VALUES (%s, %s, %s, %s)
    """, row)

# Comitar as alterações no PostgreSQL
cursor.commit()

