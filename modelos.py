import sqlite3
from conexao import conectar
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk


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
            cursor.execute('''
                INSERT INTO "TB_CLIENTE" ("NOME", "TELEFONE", "DATA_CADASTRO")
                VALUES (%s, %s, %s)
            ''', (self.nome, self.telefone, self.data_cadastro))
            conexao.commit()

            messagebox.showinfo("Cadastro", "Cliente Cadastrado com sucesso!")        

        except Exception as e:
            if "viola a restrição de unicidade" in str(e):
                messagebox.showwarning('Atenção!', 'O cliente informado já existe!')
            else:
                messagebox.showwarning('Atenção!', f'Não foi possível completar a operação.Erro: {e}')            

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
                SET "NOME" = %s,
                    "TELEFONE" = %s,
                    "DATA_CADASTRO" = %s
                    WHERE "ID_CLIENTE" = %s
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
        cursor.execute('''SELECT "ID_CLIENTE" FROM "TB_CLIENTE" WHERE "NOME" = %s''', (nome,))
        
        resultado = cursor.fetchone()
        
        conexao.close()
        if resultado:
            id = resultado[0]
            return id

        else:
            messagebox.showwarning('Cadastro', 'Cliente informado não está cadastrado.')
            #print("erro ao buscar ID_CLIENTE")

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
                condicao = '''"NOME" LIKE %s'''
            
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
                INSERT INTO "TB_TIPO_PRODUTO" ("DESCRICAO","MARGEM")
                VALUES (%s, %s)
                ''', (self.descricao,self.margem))

            conexao.commit()
            messagebox.showinfo('Cadastro', 'Tipo de Produto inserido com sucesso.')
        except Exception as e:
            if 'viola a restrição de unicidade' in str(e):
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
                UPDATE "TB_TIPO_PRODUTO"
                SET "DESCRICAO" = %s,
                    "MARGEM" = %s
                    WHERE "COD" = %s       
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
        cursor.execute('''SELECT "DESCRICAO" FROM "TB_TIPO_PRODUTO" ORDER BY "DESCRICAO" ASC''')
        descricoes = [row[0] for row in cursor.fetchall()]
        print(descricoes)
        conexao.close()

        return descricoes
    
    @staticmethod
    def localiza_tipo_produto(descricao):        
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT "COD" FROM "TB_TIPO_PRODUTO" WHERE "DESCRICAO" = %s''', (descricao,))
        
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
        cursor.execute('''SELECT * FROM "TB_TIPO_PRODUTO"''')
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
            # Inserindo os dados do fornecedor no banco
            cursor.execute('''
                INSERT INTO "TB_FORNECEDOR" ("NOME_EMPRESA", "TIPO_EMPRESA", "DATA_CADASTRO")
                VALUES (%s, %s, %s)
            ''', (self.nome_empresa, self.tipo_empresa, self.data_cadastro))

            conexao.commit()

            messagebox.showinfo('Cadastro', 'Fornecedor cadastrado com sucesso!')

        except Exception as e:
            if "viola a restrição de unicidade" in str(e):
                messagebox.showwarning('Atenção!', 'O fornecedor informado já existe!')
            else:
                messagebox.showwarning('Atenção!', f'Não foi possível completar a operação.Erro: {e}') 

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
                UPDATE "TB_FORNECEDOR"
                SET "NOME_EMPRESA" = %s,
                    "TIPO_EMPRESA" = %s,
                           "DATA_CADASTRO" = %s                   
                    WHERE "ID_FORNECEDOR" = %s
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
        cursor.execute('''SELECT * FROM "TB_FORNECEDOR"''')

        fornecedores = cursor.fetchall()

        conexao.close()
        return fornecedores

    @staticmethod
    def pesquisa_fornecedor(campo, filtro):
        conexao = conectar()
        cursor = conexao.cursor()                             
        if campo == 'Nome':
            condicao = '''"NOME_EMPRESA" LIKE %s'''
        else:
            condicao = '''"TIPO_EMPRESA" LIKE %s'''
        
        comando = '''SELECT * FROM "TB_FORNECEDOR" WHERE '''

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
        cursor.execute('''SELECT "NOME_EMPRESA" FROM "TB_FORNECEDOR" ORDER BY "NOME_EMPRESA" ASC''')
        lista_fornec = [row [0] for row in cursor.fetchall()]
        print(lista_fornec)
        conexao.close()

        return lista_fornec
    
    @staticmethod
    def localiza_id_fornecedor(nome):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT "ID_FORNECEDOR" FROM "TB_FORNECEDOR" WHERE "NOME_EMPRESA" = %s''', (nome,))
        
        resultado = cursor.fetchone()
        
        conexao.close()
        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar ID_FORNECEDOR")
    



class Produto:
    def __init__(self, nome, preco_custo, tipo_produto, fabricante, marca, cor, id_fornecedor, data_cadastro,estoque,imagem_produto, id_produto=None):
        self.id_produto = id_produto
        self.nome = nome
        self.preco_custo = preco_custo
        self.tipo_produto = tipo_produto
        self.fabricante = fabricante
        self.marca = marca
        self.cor = cor
        self.id_fornecedor = id_fornecedor
        self.data_cadastro = data_cadastro
        self.estoque = estoque
        self.imagem_produto = imagem_produto

    def salvar_produto(self):
      # Conectando ao banco de dados SQLite
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            # Inserindo os dados do cliente no banco

            cursor.execute('''
                INSERT INTO "TB_PRODUTO" ("NOME", "PRECO_CUSTO", "TIPO_PRODUTO", "FABRICANTE", "MARCA", "COR", "ID_FORNECEDOR", "DATA_CADASTRO", "ESTOQUE", "IMAGEM")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.nome, self.preco_custo, self.tipo_produto, self.fabricante, self.marca, self.cor, self.id_fornecedor, self.data_cadastro, self.estoque, self.imagem_produto))

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
        cursor.execute('''SELECT A."NOME" || '/' || A."MARCA" || '/' || B."NOME_EMPRESA", A."ID_PRODUTO" FROM "TB_PRODUTO" A
        JOIN "TB_FORNECEDOR" B ON A."ID_FORNECEDOR" = B."ID_FORNECEDOR" ORDER BY A."NOME" ASC;''')
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
                DELETE FROM "TB_PRODUTO" 
                WHERE "ID_PRODUTO" = %s
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
                UPDATE "TB_PRODUTO"
                SET "NOME" = %s,
                    "PRECO_CUSTO" = %s,
                    "TIPO_PRODUTO" = %s,
                    "FABRICANTE" = %s,
                    "MARCA" = %s,
                    "COR" = %s,
                    "ID_FORNECEDOR" = %s,
                    "ESTOQUE" = %s,
                    "IMAGEM" = %s
                    WHERE "ID_PRODUTO" = %s
            ''', (self.nome,self.preco_custo, self.tipo_produto, self.fabricante, self.marca, self.cor, self.id_fornecedor,self.estoque, self.imagem_produto, self.id_produto))

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
        cursor.execute('''SELECT A."ID_PRODUTO", A."NOME", A."PRECO_CUSTO", B."DESCRICAO", A."FABRICANTE",
                        A."MARCA", A."COR", C."NOME_EMPRESA", A."DATA_CADASTRO", A."ESTOQUE", A."IMAGEM" FROM "TB_PRODUTO" A
                        JOIN "TB_TIPO_PRODUTO" B ON B."COD" = A."TIPO_PRODUTO"
                        JOIN "TB_FORNECEDOR" C ON C."ID_FORNECEDOR" = A."ID_FORNECEDOR";''')
        
        resultado = cursor.fetchall()
        conexao.close()
        return resultado


    @staticmethod
    def localiza_produto_id(nome_produto, nome_fornecedor):    
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute('''SELECT a."ID_PRODUTO" from "TB_PRODUTO" a
                join "TB_FORNECEDOR" b on a."ID_FORNECEDOR" = b."ID_FORNECEDOR"
                where a."NOME" = %s and b."NOME_EMPRESA" = %s''', (nome_produto, nome_fornecedor,))
            
        resultado = cursor.fetchone()
        
        conexao.close()

        if resultado:
            id = resultado[0]
            return id

        else:
            print("erro ao buscar ID_PRODUTO")

    
    def pesquisar_produtos(campo, filtro):
        try:
            conexao = conectar()
            cursor = conexao.cursor()                             
            if campo == 'Nome':
                condicao = '''A."NOME" LIKE %s'''
            elif campo == 'Marca':
                condicao = '''A."MARCA" LIKE %s'''
            elif campo == 'Tipo Produto':
                condicao = '''B."DESCRICAO" LIKE %s'''
            elif campo == 'Fabricante':
                condicao = '''A."FABRICANTE" LIKE %s'''
            elif campo == 'Cor':
                condicao = '''A."COR" LIKE %s'''
            else:
                condicao = '''C."NOME_EMPRESA" LIKE %s'''

            comando = '''SELECT A."ID_PRODUTO", A."NOME", A."PRECO_CUSTO", B."DESCRICAO", A."FABRICANTE",
                            A."MARCA", A."COR", C."NOME_EMPRESA", A."DATA_CADASTRO", A."ESTOQUE" FROM "TB_PRODUTO" A
                            JOIN "TB_TIPO_PRODUTO" B ON B."COD" = A."TIPO_PRODUTO"
                            JOIN "TB_FORNECEDOR" C ON C."ID_FORNECEDOR" = A."ID_FORNECEDOR"
                            WHERE '''

            comando_final = comando + " " + condicao
            print(f'comando final: {comando_final}')
            print(f'filtro: {filtro}')
            
            cursor.execute(comando_final, ('%' + filtro + '%',))

            resultados = cursor.fetchall()
            conexao.close()
            return resultados
        except Exception as e:
            messagebox.showwarning('Cadastro', 'Não foi possível pesquisar')
        

        

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
      
        conexao = conectar()         
        try:        
            cursor = conexao.cursor()

            
            cursor.execute('''
                INSERT INTO "TB_VENDA" ("DATA", "ID_CLIENTE", "ID_PRODUTO", "QUANTIDADE", "PRECO_VENDA", "LUCRO")
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (self.data_venda, self.id_cliente, self.id_produto, self.quantidade, self.preco_venda, self.lucro))
            print(self.id_cliente)
            conexao.commit()
            messagebox.showinfo('Cadastro', 'A venda foi cadastrada com sucesso.')

        except Exception as e:
            if 'Estoque insuficiente' in str(e):
                messagebox.showwarning('Atenção', 'Não há estoque suficiente para a venda deste produto.')
            else:
                messagebox.showwarning('Atenção', f'Não foi possível completar a operação.Erro: {e}')            

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
                DELETE FROM "TB_VENDA"
                WHERE "ID" = %s
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
                UPDATE "TB_VENDA"
                SET "ID_CLIENTE" = %s,
                    "ID_PRODUTO" = %s,
                    "QUANTIDADE" = %s,
                    "PRECO_VENDA" = %s,
                    "LUCRO" = %s
                    WHERE "ID" = %s
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
    def calcular_margem(nome_produto):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT A."MARGEM" FROM "TB_TIPO_PRODUTO" A 
                       JOIN "TB_PRODUTO" B ON A."COD" = B."TIPO_PRODUTO"
                       WHERE B."NOME"= %s''', (nome_produto,))
        
        margem = float(cursor.fetchone()[0])
                
        if margem:
            return margem        
            
    @staticmethod
    def calcular_preco_sugerido(nome_produto, nome_fornecedor):     
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''select a."PRECO_CUSTO", c."MARGEM" from "TB_PRODUTO" a
                join "TB_FORNECEDOR" b on a."ID_FORNECEDOR" = b."ID_FORNECEDOR"
                join "TB_TIPO_PRODUTO" C on a."TIPO_PRODUTO" = c."COD"
                where a."NOME" = %s and b."NOME_EMPRESA" = %s''', (nome_produto, nome_fornecedor,))
            
        resultado = cursor.fetchone()
        
        preco_custo = float(resultado[0])
        margem = float(resultado[1])        
        valor_total = preco_custo + margem       
        conexao.close()

        if resultado:            
            valor = str(valor_total)
            valor_formatado = valor.replace('.', ',')
            
            return valor_formatado

        else:
            print("erro ao buscar ID_PRODUTO")

    def pesquisar_venda(campo, filtro, datas):
        conexao = conectar()
        cursor = conexao.cursor()                             
        if campo == 'Cliente':
            condicao = '''B."NOME" LIKE %s'''
        elif campo == 'Fornecedor':
            condicao = '''D."NOME_EMPRESA" LIKE %s'''
        else:
            condicao = '''C."NOME" LIKE %s'''

        condicao = condicao + ''' AND "DATA" BETWEEN %s AND %s'''

        comando = '''SELECT A."ID", A."DATA", B."NOME", C."NOME" || '/' || C."MARCA" || '/' || D."NOME_EMPRESA" as Produto, a."QUANTIDADE", a."PRECO_VENDA", a."LUCRO"
                        from "TB_VENDA" a
                        join "TB_CLIENTE" b on a."ID_CLIENTE" = b."ID_CLIENTE"
                        join "TB_PRODUTO" c on a."ID_PRODUTO" = c."ID_PRODUTO"
                        join "TB_FORNECEDOR" d on c."ID_FORNECEDOR" = d."ID_FORNECEDOR"
                        WHERE'''
        comando_final = comando + " " + condicao
        print(comando_final)
        print(filtro)
        print(datas[0])
        print(datas[1])                      
        cursor.execute(comando_final, ('%' + filtro + '%', datas[0], datas[1],))
        resultado = cursor.fetchall()
        
        conexao.close()
        return resultado
    
    @staticmethod
    def carregar_vendas_treeview():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''select a."ID", a."DATA", b."NOME", c."NOME" || '/' || c."MARCA" || '/'|| d."NOME_EMPRESA" as Produto, a."QUANTIDADE", a."PRECO_VENDA", a."LUCRO"
                        from "TB_VENDA" a
                        join "TB_CLIENTE" b on a."ID_CLIENTE" = b."ID_CLIENTE"
                        join "TB_PRODUTO" c on a."ID_PRODUTO" = c."ID_PRODUTO"
                        join "TB_FORNECEDOR" d on c."ID_FORNECEDOR" = d."ID_FORNECEDOR";''')
        resultados = cursor.fetchall()
        conexao.close()
        return resultados
    
class Combobox_filtravel(ttk.Combobox):
    def set_completion_list(self, completion_list, min_chars=3):
        self._completion_list = sorted(completion_list)  # Lista completa de itens
        #self.filtered_list = self._completion_list  # Inicializa a lista filtrada
        self.min_chars = min_chars  # Quantidade mínima de caracteres
        self.configure(values=self._completion_list)
        self.bind('<KeyRelease>', self._on_keyrelease)
        #self.bind('<FocusOut>', self._reset)  # Reseta a lista completa ao perder o foco
        #self.bind("<<ComboboxSelected>>", self._update_value)  # Atualiza valor corretamente
    
    def _on_keyrelease(self, event):
        """ Manipula o evento de digitação para filtrar a lista sem exibir a lista suspensa. """
        #if event.keysym in ("BackSpace", "Left", "Right", "Up", "Down"):
            #return
        
        # Captura o valor digitado e sua posição
        value = self.get().lower()

        if value == '':
            self.configure(values=self._completion_list)
        else:
            data = []
            for item in self._completion_list:
                if value.lower() in item.lower():
                    data.append(item)
                
            self.configure(values=data)
    #         data = []
    #         for item in lista_clientes:
    #             if valor.upper() in item.upper():
    #                 data.append(item)
            
    #         combo_cliente["value"] = data
        #cursor_position = self.index(tk.INSERT)

        # Só filtra se o valor tiver o mínimo de caracteres especificado
        if len(value) < self.min_chars:
            self.filtered_list = self._completion_list  # Exibe lista completa
            self.configure(values=self._completion_list)  # Não abre a lista suspensa
        else:
            # Filtra os itens da lista
            self.filtered_list = [item for item in self._completion_list if value in item.lower()]

            # Atualiza a lista de valores do combobox, mas não exibe a lista suspensa
            self.configure(values=self.filtered_list)

        # Reposiciona o cursor corretamente
        #self.icursor(cursor_position)

    #def _reset(self, event):
        """ Reseta os valores da combobox ao perder o foco """
       # self.configure(values=self._completion_list)

    #def _update_value(self, event):
        """ Atualiza o valor da Combobox baseado na lista filtrada. """
       # value = self.get().upper()  # Captura o valor atual selecionado
       # if value in self.filtered_list:
         #   self.set(value) # Atualiza a combobox com o valor correto
       # else:
           # self.set('')  # Se o valor não estiver na lista filtrada, limpa o campo
        
