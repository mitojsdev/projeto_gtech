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



def localiza_produto_id(nome_produto, nome_fornecedor, contexto):    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''select a.id_produto from TB_PRODUTO_NEW a
            join TB_FORNECEDOR b on a.ID_FORNECEDOR = b.ID_FORNECEDOR
            where a.NOME = ? and b.NOME_EMPRESA = ?''', (nome_produto, nome_fornecedor,))
        
    resultado = cursor.fetchone()
    
    conexao.close()

    if resultado:
        id = resultado[0]
        return id

    else:
        print("erro ao buscar ID_PRODUTO")



def calcular_preco_sugerido(nome_produto, nome_fornecedor):     
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''select a.preco_custo +100 from TB_PRODUTO_NEW a
            join TB_FORNECEDOR b on a.ID_FORNECEDOR = b.ID_FORNECEDOR
            where a.NOME = ? and b.NOME_EMPRESA = ?''', (nome_produto, nome_fornecedor,))
        
    resultado = cursor.fetchone()
    
    conexao.close()

    if resultado:
        valor = resultado[0]
        return valor

    else:
        print("erro ao buscar ID_PRODUTO")

    

          