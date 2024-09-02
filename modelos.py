import sqlite3
from conexao import conectar

class Cliente:
    def __init__(self, id_cliente, nome, telefone, data_cadastro):
        self.id = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.data_cadastro = data_cadastro

    def salvar_no_banco(self):
        # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Inserindo os dados do cliente no banco
            cursor.execute('''
                INSERT INTO TB_CLIENTE (id_cliente, nome, telefone, data_cadastro)
                VALUES (?, ?, ?, ?)
            ''', (self.id, self.nome, self.telefone, self.data_cadastro))

            conexao.commit()

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()
            


class TipoProduto:
    def __init__(self, descricao):                
        self.descricao = descricao

    def salvar_no_banco(self):
        # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            cursor.execute('''select Max(COD) + 1 from TB_TIPO_PRODUTO''')

            resultado = cursor.fetchone()
            print(resultado)
            if resultado:                
                prox_cod = resultado[0]
                print(prox_cod)

                # Inserindo tipo_produto no banco
                cursor.execute('''
                INSERT INTO TB_TIPO_PRODUTO (cod, descricao)
                VALUES (?,?)
                ''', (prox_cod, self.descricao))

                conexao.commit()

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()

class Fornecedor:
    def __init__(self, id_fornecedor, nome_empresa, tipo_empresa):
        self.id_fornecedor = id_fornecedor
        self.nome_empresa = nome_empresa
        self.tipo_empresa = tipo_empresa


class Produto:
    def __init__(self, id_produto, nome, preco_custo, id_tipo_produto, fabricante, marca, cor, id_fornecedor, data_cadastro):
        self.id_produto = id_produto
        self.nome = nome
        self.preco_custo = preco_custo
        self.tipo_produto = id_tipo_produto
        self.fabricante = fabricante
        self.marca = marca
        self.cor = cor
        self.id_fornecedor = id_fornecedor
        self.data_cadastro = data_cadastro


class Venda:
    def __init__(self, id_venda, data_venda, id_cliente, id_produto, quantidade, preco_venda, lucro):
        self.id_venda = id_venda
        self.data_venda = data_venda
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_venda = preco_venda
        self.lucro = lucro
