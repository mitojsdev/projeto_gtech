import sqlite3
import psycopg2

# Conexão com o banco de dados SQLite3
sqlite_conn = sqlite3.connect('./Banco/BancoGtech.db')
sqlite_cur = sqlite_conn.cursor()

# Conexão com o banco de dados PostgreSQL
#conn = psycopg2.connect(database="localhost", user="root", password="root")
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="root",
    
)

cursor = conn.cursor()


# Seleciona todos os dados da tabela no SQLite
sqlite_cur.execute("SELECT * FROM TB_VENDA")
dados_sqlite = sqlite_cur.fetchall()
print(dados_sqlite)

#CREATE TABLE "TB_VENDA" ( ID INT NOT NULL, DATA DATE NOT NULL, ID_CLIENTE INT, ID_PRODUTO INT, QUANTIDADE INT, PRECO_VENDA FLOAT NOT NULL, LUCRO FLOAT, PRIMARY KEY (ID), FOREIGN KEY(ID_CLIENTE) REFERENCES TB_CLIENTE (ID_CLIENTE), FOREIGN KEY(ID_PRODUTO) REFERENCES TB_PRODUTO_NEW (ID_PRODUTO) )
for row in dados_sqlite:
    cursor.execute("""
        INSERT INTO "TB_VENDA" ("ID", "DATA", "ID_CLIENTE","ID_PRODUTO", "QUANTIDADE", "PRECO_VENDA", "LUCRO")
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, row)
    

# Comitar as alterações no PostgreSQL
conn.commit()


