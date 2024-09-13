import sqlite3
from conexao import conectar
from tkinter import messagebox


class Cliente:
    def __init__(self, nome, telefone, data_cadastro, id_cliente=None):
        self.id = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.data_cadastro = data_cadastro

    

    def salvar_cliente(self):
        # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()
            
            #etapa 1 verificar se o cliente já existe (analisar os campos nome e telefone)
            #cursor postgree
            #cursor.execute('''SELECT * FROM "TB_CLIENTE" WHERE "NOME" = %s AND "TELEFONE" = %s''', 
             #              (self.nome,self.telefone,))
            #cursor sqlite
            cursor.execute('''SELECT * FROM "TB_CLIENTE" WHERE "NOME" = ? AND "TELEFONE" = ?''', 
                           (self.nome,self.telefone,))
            resultado = cursor.fetchall()
            tamanho = len(resultado)            
            if tamanho != 0:
                messagebox.showwarning('Atenção!', 'Já existe um cliente cadastrado com os dados informados.')
            else:
                #etapa 2, se nao for repetido, inserir dados            
                # Inserindo os dados do cliente no banco
                #cursor postgre
                #cursor.execute('''
                    #INSERT INTO "TB_CLIENTE" ("NOME", "TELEFONE", "DATA_CADASTRO")
                   #VALUES (%s, %s, %s)
                #''', (self.nome, self.telefone, self.data_cadastro))
                #cursor sqlite
                cursor.execute('''
                    INSERT INTO "TB_CLIENTE" ("NOME", "TELEFONE", "DATA_CADASTRO")
                    VALUES (?, ?, ?)
                ''', (self.nome, self.telefone, self.data_cadastro))
                conexao.commit()

                messagebox.showinfo("Cadastro", "Cliente Cadastrado com sucesso!")        

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()


    def alterar_cliente(self):
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()
            comando = '''
                UPDATE "TB_CLIENTE" 
                SET "NOME" = ?,
                    "TELEFONE" = ?,
                    "DATA_CADASTRO" = ?
                    WHERE "ID_CLIENTE" = ?
            '''
            # Altearando os dados do cliente no banco
            cursor.execute(comando, (self.nome,self.telefone,self.data_cadastro,self.id))
            
            print(self.nome)
            print(self.telefone)
            print(self.id)
            conexao.commit()
            messagebox.showinfo("Cadastro", "Cliente alterado.")

        except Exception as e:
            messagebox.showerror("Cadastro", f"Não foi possível completar a operação. Erro: {e}")
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()

    def carregar_clientes_combo():
        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT "NOME" FROM "TB_CLIENTE" ORDER BY "NOME" ASC''')
        lista_cli = [row [0] for row in cursor.fetchall()]
        print(lista_cli)
        conexao.close()

        return lista_cli

    @staticmethod
    def localiza_id_cliente(nome):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT "ID_CLIENTE" FROM "TB_CLIENTE" WHERE "NOME" = ?''', (nome,))
        
        resultado = cursor.fetchone()
        
        conexao.close()
        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar ID_CLIENTE")

    @staticmethod
    def carregar_clientes_treeview():
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute('''SELECT * FROM "TB_CLIENTE"''')

        clientes = cursor.fetchall()

        return clientes
    
    @staticmethod
    def pesquisa_clientes(campo, filtro):
        try:
            conexao = conectar()
            cursor = conexao.cursor()                             
            if campo == 'Nome':
                condicao = '''"NOME" LIKE ?'''
            
            comando = '''SELECT * FROM "TB_CLIENTE" WHERE '''

            comando_final = comando + " " + condicao
            print(f'comando final: {comando_final}')
            print(f'filtro: {filtro}')
            
            cursor.execute(comando_final, ('%' + filtro + '%',))

            resultados = cursor.fetchall()

            return resultados
        except Exception as e:
            messagebox.showerror("Cadastro", f"Atenção! Não foi possível pesquisar. Erro: {e}")


class TipoProduto:
    def __init__(self, descricao, margem, id_tipo_produto=None):                
        self.descricao = descricao
        self.margem = margem
        self.id_tipo_produto = id_tipo_produto

    def salvar_no_banco(self):
        # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            cursor.execute('''
                INSERT INTO TB_TIPO_PRODUTO (DESCRICAO, MARGEM)
                VALUES (?, ?)
                ''', (self.descricao,self.margem))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'Tipo de Produto inserido com sucesso.')
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                messagebox.showwarning('Atenção!', 'Este Tipo de produto já existe.')
            else:
                messagebox.showwarning('Cadastro', f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()
    
    def alterar_no_banco(self):
        # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()
            
            cursor.execute('''
                UPDATE TB_TIPO_PRODUTO
                SET DESCRICAO = ?,
                    MARGEM = ?
                    WHERE COD = ?       
                ''', (self.descricao,self.margem, self.id_tipo_produto))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'Tipo de Produto alterado com sucesso.')

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()
                
    def carregar_tipos_produto():
        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT DESCRICAO FROM TB_TIPO_PRODUTO ORDER BY DESCRICAO ASC''')
        descricoes = [row[0] for row in cursor.fetchall()]
        print(descricoes)
        conexao.close()

        return descricoes
    
    @staticmethod
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
    @staticmethod
    def carregar_tipos_produto_treeview():
         # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM TB_TIPO_PRODUTO")
        tipos = cursor.fetchall()

        conexao.close()
        return tipos
    

class Fornecedor:
    def __init__(self, nome_empresa, tipo_empresa, data_cadastro, id_fornecedor=None):
        self.id_fornecedor = id_fornecedor
        self.nome_empresa = nome_empresa
        self.tipo_empresa = tipo_empresa
        self.data_cadastro = data_cadastro

    def salvar_fornecedor(self):
        # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            cursor.execute('''SELECT * FROM "TB_FORNECEDOR" WHERE "NOME_EMPRESA" = ? AND "TIPO_EMPRESA" = ?''', 
                           (self.nome_empresa,self.tipo_empresa,))
            resultado = cursor.fetchall()
            tamanho = len(resultado)            
            if tamanho != 0:
                messagebox.showwarning('Atenção!', 'Já existe um fornecedor cadastrado com os dados informados.')
            else:

            # Inserindo os dados do cliente no banco
                cursor.execute('''
                    INSERT INTO TB_FORNECEDOR (nome_empresa, tipo_empresa, data_cadastro)
                    VALUES (?, ?, ?)
                ''', (self.nome_empresa, self.tipo_empresa, self.data_cadastro))

                conexao.commit()

                messagebox.showinfo('Cadastro', 'Fornecedor cadastrado com sucesso!')

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()
    
    def alterar_fornecedor(self):
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Altearando os dados do cliente no banco
            cursor.execute('''
                UPDATE TB_FORNECEDOR 
                SET NOME_EMPRESA = ?,
                    TIPO_EMPRESA = ?,
                           DATA_CADASTRO = ?                   
                    WHERE ID_FORNECEDOR = ?
            ''', (self.nome_empresa,self.tipo_empresa, self.data_cadastro,self.id_fornecedor))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'O fornecedor foi alterado.')
        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()

    @staticmethod
    def carregar_fornecedores_treeview():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM TB_FORNECEDOR")

        fornecedores = cursor.fetchall()

        conexao.close()
        return fornecedores

    @staticmethod
    def pesquisa_fornecedor(campo, filtro):
        conexao = conectar()
        cursor = conexao.cursor()                             
        if campo == 'Nome':
            condicao = '''NOME_EMPRESA LIKE ?'''
        else:
            condicao = '''TIPO_EMPRESA LIKE ?'''
        
        comando = '''SELECT * FROM TB_FORNECEDOR WHERE '''

        comando_final = comando + " " + condicao
        print(f'comando final: {comando_final}')
        print(f'filtro: {filtro}')
        
        cursor.execute(comando_final, ('%' + filtro + '%',))

        resultados = cursor.fetchall()
        conexao.close()
        return resultados

    def carregar_fornecedores_combo():
        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT NOME_EMPRESA FROM TB_FORNECEDOR ORDER BY NOME_EMPRESA ASC")
        lista_fornec = [row [0] for row in cursor.fetchall()]
        print(lista_fornec)
        conexao.close()

        return lista_fornec
    
    @staticmethod
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
    



class Produto:
    def __init__(self, nome, preco_custo, tipo_produto, fabricante, marca, cor, id_fornecedor, data_cadastro, id_produto=None):
        self.id_produto = id_produto
        self.nome = nome
        self.preco_custo = preco_custo
        self.tipo_produto = tipo_produto
        self.fabricante = fabricante
        self.marca = marca
        self.cor = cor
        self.id_fornecedor = id_fornecedor
        self.data_cadastro = data_cadastro

    def salvar_produto(self):
      # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Inserindo os dados do cliente no banco

            cursor.execute('''
                INSERT INTO TB_PRODUTO (NOME, PRECO_CUSTO, TIPO_PRODUTO, FABRICANTE, MARCA, COR, ID_FORNECEDOR, DATA_CADASTRO)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.preco_custo, self.tipo_produto, self.fabricante, self.marca, self.cor, self.id_fornecedor, self.data_cadastro))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'Produto inserido com sucesso!')

        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                messagebox.showwarning('Cadastro', 'Este produto já existe para esse fornecedor.')
            else:
                messagebox.showwarning('Cadastro', f'Não foi possível completar a operação.Erro: {e}')
            

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()  
        

    def carregar_produtos_combo():
        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT A.NOME || '/' || A.MARCA || '/' || B.NOME_EMPRESA, A.ID_PRODUTO FROM TB_PRODUTO A
        JOIN TB_FORNECEDOR B ON A.ID_FORNECEDOR = B.ID_FORNECEDOR ORDER BY A.NOME ASC;''')
        lista_produtos = [row [0] for row in cursor.fetchall()]
        print(lista_produtos)
        conexao.close()

        return lista_produtos
    
    def excluir_produto(self):
      # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Excluindo os dados do cliente no banco
            cursor.execute('''
                DELETE FROM TB_PRODUTO_NEW 
                WHERE ID_PRODUTO = ?
            ''', (self.id_produto,))

            conexao.commit()

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()
    
    def alterar_produto(self):
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Excluindo os dados do cliente no banco
            cursor.execute('''
                UPDATE TB_PRODUTO
                SET NOME = ?,
                    PRECO_CUSTO = ?,
                    TIPO_PRODUTO = ?,
                    FABRICANTE = ?,
                    MARCA = ?,
                    COR = ?,
                    ID_FORNECEDOR = ?
                    WHERE ID_PRODUTO = ?
            ''', (self.nome,self.preco_custo, self.tipo_produto, self.fabricante, self.marca, self.cor, self.id_fornecedor, self.id_produto))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'O produto foi alterado.')
        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()

    @staticmethod
    def carregar_produtos_treeview():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT A.ID_PRODUTO, A.NOME, A.PRECO_CUSTO, B.DESCRICAO, A.FABRICANTE,
                        A.MARCA, A.COR, C.NOME_EMPRESA, A.DATA_CADASTRO FROM TB_PRODUTO A
                        JOIN TB_TIPO_PRODUTO B ON B.COD = A.TIPO_PRODUTO
                        JOIN TB_FORNECEDOR C ON C.ID_FORNECEDOR = A.ID_FORNECEDOR;''')
        
        resultado = cursor.fetchall()
        conexao.close()
        return resultado


    @staticmethod
    def localiza_produto_id(nome_produto, nome_fornecedor):    
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute('''select a.id_produto from TB_PRODUTO a
                join TB_FORNECEDOR b on a.ID_FORNECEDOR = b.ID_FORNECEDOR
                where a.NOME = ? and b.NOME_EMPRESA = ?''', (nome_produto, nome_fornecedor,))
            
        resultado = cursor.fetchone()
        
        conexao.close()

        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar ID_PRODUTO")

    
    def pesquisar_produtos(campo, filtro):
        conexao = conectar()
        cursor = conexao.cursor()                             
        if campo == 'Nome':
            condicao = '''A.NOME LIKE ?'''
        elif campo == 'Marca':
            condicao = '''A.MARCA LIKE ?'''
        elif campo == 'Tipo Produto':
            condicao = '''B.DESCRICAO LIKE ?'''
        elif campo == 'Fabricante':
            condicao = '''A.FABRICANTE LIKE ?'''
        elif campo == 'Cor':
            condicao = '''A.COR LIKE ?'''
        else:
            condicao = '''C.NOME_EMPRESA LIKE ?'''

        comando = '''SELECT A.ID_PRODUTO, A.NOME, A.PRECO_CUSTO, B.DESCRICAO, A.FABRICANTE,
                        A.MARCA, A.COR, C.NOME_EMPRESA, A.DATA_CADASTRO FROM TB_PRODUTO A
                        JOIN TB_TIPO_PRODUTO B ON B.COD = A.TIPO_PRODUTO
                        JOIN TB_FORNECEDOR C ON C.ID_FORNECEDOR = A.ID_FORNECEDOR
                        WHERE '''

        comando_final = comando + " " + condicao
        print(f'comando final: {comando_final}')
        print(f'filtro: {filtro}')
        
        cursor.execute(comando_final, ('%' + filtro + '%',))

        resultados = cursor.fetchall()
        conexao.close()
        return resultados

        

class Venda:
    def __init__(self, data_venda, id_cliente, id_produto, quantidade, preco_venda, lucro, id_venda=None):
        self.id_venda = id_venda
        self.data_venda = data_venda
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_venda = preco_venda
        self.lucro = lucro

    def salvar_venda(self):
      # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Inserindo os dados do cliente no banco
            cursor.execute('''
                INSERT INTO TB_VENDA(DATA, ID_CLIENTE, ID_PRODUTO, QUANTIDADE, PRECO_VENDA, LUCRO)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.data_venda, self.id_cliente, self.id_produto, self.quantidade, self.preco_venda, self.lucro))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'A venda foi cadastrada com sucesso.')

        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()  
    
    def excluir_venda(self):
      # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Excluindo os dados do cliente no banco
            cursor.execute('''
                DELETE FROM TB_VENDA 
                WHERE ID = ?
            ''', (self.id_venda,))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'A venda foi excluída com sucesso')

        except Exception as e:
            messagebox.showinfo('Cadastro', f'Não foi possível completar a operação.Erro: {e}')
           

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()
    
    def alterar_venda(self):
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Excluindo os dados do cliente no banco
            cursor.execute('''
                UPDATE TB_VENDA 
                SET ID_CLIENTE = ?,
                    ID_PRODUTO = ?,
                    QUANTIDADE = ?,
                    PRECO_VENDA = ?,
                    LUCRO = ?
                    WHERE ID = ?
            ''', (self.id_cliente,self.id_produto, self.quantidade, self.preco_venda, self.lucro, self.id_venda))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'A venda foi alterada com sucesso.')
        except Exception as e:
            print(f'Não foi possível completar a operação.Erro: {e}')

        finally:
            # Salvando (commit) as mudanças e fechando a conexão
            if conexao:
                cursor.close()                
                conexao.close()

    @staticmethod
    def calcular_preco_sugerido(nome_produto, nome_fornecedor):     
        conexao = conectar()
        cursor = conexao.cursor()
    #implementar aqui a lógica do lucro dependendo do tipo_produto
    #   
        
        cursor.execute('''select a.preco_custo, c.margem from TB_PRODUTO a
                join TB_FORNECEDOR b on a.ID_FORNECEDOR = b.ID_FORNECEDOR
                join TB_TIPO_PRODUTO C on a.TIPO_PRODUTO = c.COD
                where a.NOME = ? and b.NOME_EMPRESA = ?''', (nome_produto, nome_fornecedor,))
            
        resultado = cursor.fetchone()
        
        preco_custo = float(resultado[0])
        margem = float(resultado[1])
        print(resultado)
        valor_total = preco_custo + margem
        conexao.close()

        if resultado:            
            valor = str(valor_total)
            valor_formatado = valor.replace('.', ',')
            
            return valor_formatado

        else:
            print("erro ao buscar ID_PRODUTO")

    def pesquisar_venda(campo, filtro):
        conexao = conectar()
        cursor = conexao.cursor()                             
        if campo == 'Cliente':
            condicao = '''B.NOME LIKE ?'''
        elif campo == 'Fornecedor':
            condicao = '''D.NOME_EMPRESA LIKE ?'''
        else:
            condicao = '''C.NOME LIKE ?'''

        comando = '''SELECT A.ID, A.DATA, B.NOME, C.NOME || '/' || C.MARCA || '/' || D.NOME_EMPRESA as Produto, a.QUANTIDADE, a.PRECO_VENDA, a.LUCRO
                        from TB_VENDA a
                        join TB_CLIENTE b on a.ID_CLIENTE = b.ID_CLIENTE
                        join TB_PRODUTO c on a.ID_PRODUTO = c.ID_PRODUTO
                        join TB_FORNECEDOR d on c.ID_FORNECEDOR = d.ID_FORNECEDOR
                        WHERE'''
        comando_final = comando + " " + condicao                
        cursor.execute(comando_final, ('%' + filtro + '%',))
        resultado = cursor.fetchall()
        
        conexao.close()
        return resultado
    
    @staticmethod
    def carregar_vendas_treeview():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''select a.id, a.DATA, b.NOME, c.NOME || '/' || c.MARCA || '/'|| d.NOME_EMPRESA as Produto, a.QUANTIDADE, a.PRECO_VENDA, a.LUCRO
                        from TB_VENDA a
                        join TB_CLIENTE b on a.ID_CLIENTE = b.ID_CLIENTE
                        join TB_PRODUTO c on a.ID_PRODUTO = c.ID_PRODUTO
                        join TB_FORNECEDOR d on c.ID_FORNECEDOR = d.ID_FORNECEDOR;''')
        resultados = cursor.fetchall()
        conexao.close()
        return resultados
