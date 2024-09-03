import sqlite3
print("iniciando...")

def conectar():
    try:

    #conectando ao banco de dados
        #conexao = sqlite3.connect('./Banco/BancoGtech.db')
        conexao = sqlite3.connect('C:/Users/amilt/Documents/GTECH_NEW/Banco/BancoGtech.db')
        conexao.execute("PRAGMA foreign_keys = on") 
        


        return conexao
    

    except Exception as erro:
            print(f"Ocorreu um erro ao conectar o banco de dados: {erro}")

