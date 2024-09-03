from conexao import conectar

def localiza_tipo_produto(descricao):        
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COD FROM TB_TIPO_PRODUTO WHERE DESCRICAO = ?", (descricao,))
        
        resultado = cursor.fetchone()
        

        conexao.close()
        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar COD PRODUTO")

def localiza_id_fornecedor(nome):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT ID_FORNECEDOR FROM TB_FORNECEDOR WHERE NOME_EMPRESA = ?", (nome,))
        
        resultado = cursor.fetchone()
        
        conexao.close()
        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar ID_FORNECEDOR")

def localiza_cliente_id(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT ID_CLIENTE FROM TB_CLIENTE WHERE NOME = ?", (nome,))
        
    resultado = cursor.fetchone()
        
    conexao.close()
    if resultado:
        id = resultado[0]
        return id

    else:
        print("erro ao buscar ID_CLIENTE")



def localiza_produto_id(nome_produto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT ID_PRODUTO FROM TB_PRODUTO_NEW WHERE NOME = ?", (nome_produto,))
        
    resultado = cursor.fetchone()
        
    conexao.close()
    if resultado:
        id = resultado[0]
        return id

    else:
        print("erro ao buscar ID_PRODUTO")