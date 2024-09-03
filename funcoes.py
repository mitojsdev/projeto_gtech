from conexao import conectar
def localiza_tipo_produto(descricao):        
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COD FROM TB_TIPO_PRODUTO WHERE DESCRICAO = ?", (descricao))
        
        resultado = cursor.fetchone()
        print(resultado[0])

        conexao.close()
        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar COD PRODUTO")