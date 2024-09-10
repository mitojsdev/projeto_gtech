#import funcoes as fct
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from modelos import Cliente  # Importando a Classe Cliente
from modelos import TipoProduto
from modelos import Fornecedor
from modelos import Produto
from modelos import Venda
from conexao import conectar
from tkinter import PhotoImage
from views import cadastrar_cliente
#from funcoes import localiza_tipo_produto, localiza_id_fornecedor, localiza_cliente_id, localiza_produto_id
valor_sugerido = 0

import os

######################################################################################
# Função para abrir a tela de cadastro de Tipo Produto
def cadastrar_tipo_produto():
    # Nova janela para cadastro de cliente
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Tipos de Produto")
    cadastro_janela.geometry("450x450")

    # Campos de entrada    
    tk.Label(cadastro_janela, text="Descrição").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    
    txt_descricao = tk.Entry(cadastro_janela)
    txt_descricao.grid(row=0, column=1, padx=9, pady=0, sticky="w")


    # Função para salvar o cliente
    def salvar_tipo_produto():        
        tipo_produto = txt_descricao.get()        

        # Instanciando a classe Cliente
        tipoDeProduto = TipoProduto(tipo_produto)        
        tipoDeProduto.salvar_no_banco()
        # Adicionando o cliente à treeview
        #treeview.insert("", "end", values=(id_cliente, nome, telefone, data_cadastro))

        messagebox.showinfo("Cadastro", "Tipo de Produto inserido com sucesso.")

    # Botão para salvar o cliente
    tk.Button(cadastro_janela, text="Salvar", command=salvar_tipo_produto).grid(row=2, columnspan=2, pady=10)

    # Criando a Treeview para exibir os clientes cadastrados
    columns = ("Cod", "Descricao")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("Cod", text="Cod")
    treeview.heading("Descricao", text="Descricao")    
    treeview.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def carregar_tipo_produto():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM TB_TIPO_PRODUTO")
        tipos = cursor.fetchall()

        # Adicionando os dados na Treeview
        for tipo in tipos:
            treeview.insert("", "end", values=tipo)
        
        conexao.close()

    # Carregar clientes ao abrir a janela
    carregar_tipo_produto()
######################################################################################

######################################################################################
#função para cadastrar fornecedor
def cadastrar_fornecedor():
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Fornecedor")
    cadastro_janela.geometry("850x450")

    
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome Empresa").grid(row=1, column=0, padx=10, pady=5, sticky="e")    
    tk.Label(cadastro_janela, text="Tipo Empresa").grid(row=2, column=0, padx=10, pady=5, sticky="e") 
    tk.Label(cadastro_janela, text="Data Cadastro").grid(row=3, column=0, padx=10, pady=5, sticky="e") 
    lbl_filtrar =tk.Label(cadastro_janela, text="Filtrar")
    lbl_filtrar.grid(row=4, column=1, padx=0, pady=5, sticky="e")
    lbl_campo =tk.Label(cadastro_janela, text="Selecione:")
    lbl_campo.grid(row=3, column=1, padx=0, pady=5, sticky="e")

    txt_id = tk.Entry(cadastro_janela)
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome_empresa = tk.Entry(cadastro_janela)
    txt_nome_empresa.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tipos_empresa = ['Física', 'Virtual', 'Outro']    
    combo_tipo_empresa = ttk.Combobox(cadastro_janela, values=tipos_empresa)
    combo_tipo_empresa.current(0)
    combo_tipo_empresa.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    lista_campos = ['Nome', 'Tipo Empresa']
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos)
    combo_pesquisa.grid(row=3, column=2, padx=10, pady=5, sticky="w")
    
    def salvar_fornecedor(operacao):
        id = int(txt_id.get())
        nome = txt_nome_empresa.get()
        tipo_empresa = combo_tipo_empresa.get()
        data_cadastro = txt_data_cadastro.get()

        
        fornecedor = Fornecedor(id, nome, tipo_empresa, data_cadastro)
        if operacao == 'I':
            fornecedor.salvar_fornecedor()

            messagebox.showinfo("Cadastro", "Produto Cadastrado.")        
        else:
            fornecedor.alterar_fornecedor()
            messagebox.showinfo("Cadastro", "Produto alterado.")
        
        carregar_fornecedores()        
                

    
    #tk.Button(cadastro_janela, text="Salvar", command=salvar_fornecedor).grid(row=4, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_fornecedor('I')).grid(row=4, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_fornecedor('A')).grid(row=4, columnspan=3, pady=10)
    
    columns = ("ID", "Nome Empresa", "Tipo Empresa", "Data de Cadastro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Nome Empresa", text="Nome Empresa")
    treeview.heading("Tipo Empresa", text="Tipo Empresa")
    treeview.heading("Data de Cadastro", text="Data de Cadastro")
    treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def carregar_fornecedores():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM TB_FORNECEDOR")
        fornecedores = cursor.fetchall()

        # Adicionando os dados na Treeview
        for fornecedor in fornecedores:
            treeview.insert("", "end", values=fornecedor)
        
        conexao.close()

    # Carregar clientes ao abrir a janela
    carregar_fornecedores()
    #ID", "Nome Empresa", "Tipo Empresa", "Data de Cadastro")
    def ao_clicar_treeview(event):
        item_selecionado = treeview.selection()

        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])

            txt_nome_empresa.delete(0,tk.END)
            txt_nome_empresa.insert(0,item[1])

            combo_tipo_empresa.set(item[2])

            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[3])
                        
    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get()
        #Nome, TIPO EMPRESA
        for item in treeview.get_children():
            treeview.delete(item)
        
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
        
        for resultado in resultados:
            treeview.insert("", "end", values=resultado)

        conexao.close()
######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)

######################################################################################

######################################################################################
#função para cadastrar Produtos
def cadastrar_produto():
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Produto")
    cadastro_janela.geometry("1200x650")

    
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome").grid(row=1, column=0, padx=10, pady=5, sticky="e")    
    tk.Label(cadastro_janela, text="Preço Custo").grid(row=2, column=0, padx=10, pady=5, sticky="e") 
    tk.Label(cadastro_janela, text="Tipo Produto").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Fabricante").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Marca").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Cor").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Fornecedor").grid(row=7, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Data Cadastro").grid(row=8, column=0, padx=10, pady=5, sticky="e")
    lbl_filtrar =tk.Label(cadastro_janela, text="Filtrar")
    lbl_filtrar.grid(row=9, column=1, padx=0, pady=5, sticky="e")
    lbl_campo =tk.Label(cadastro_janela, text="Selecione:")
    lbl_campo.grid(row=8, column=1, padx=0, pady=5, sticky="e")


    txt_id = tk.Entry(cadastro_janela)
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome = tk.Entry(cadastro_janela)
    txt_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    txt_preco_custo = tk.Entry(cadastro_janela)
    txt_preco_custo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tipos_produto = TipoProduto.carregar_tipos_produto()    
    combo_tipo_produto = ttk.Combobox(cadastro_janela, values=tipos_produto)
    combo_tipo_produto.current(0)
    combo_tipo_produto.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    txt_fabricante = tk.Entry(cadastro_janela)
    txt_fabricante.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    
    txt_marca = tk.Entry(cadastro_janela)
    txt_marca.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    txt_cor = tk.Entry(cadastro_janela)
    txt_cor.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    lista_fornecedores = Fornecedor.carregar_fornecedores_combo()
    combo_fornecedor = ttk.Combobox(cadastro_janela, values=lista_fornecedores)
    combo_fornecedor.current(0)
    combo_fornecedor.grid(row=7, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=8, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=9, column=2, padx=10, pady=5, sticky="w")

    lista_campos = ['Nome', 'Marca', 'Tipo Produto', 'Fabricante','Cor','Fornecedor']
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos)
    combo_pesquisa.grid(row=8, column=2, padx=10, pady=5, sticky="w")
    
    def salvar_produto(operacao):
        id = int(txt_id.get())
        print(id)
        nome = txt_nome.get()
        print(nome)
        preco_custo = float(txt_preco_custo.get())
        print(preco_custo)
        tipo_produto = combo_tipo_produto.get()
        print(tipo_produto)        
        tipo_produto_id = TipoProduto.localiza_tipo_produto(tipo_produto)
        print(tipo_produto_id)
        print(type(tipo_produto_id))
        fabricante = txt_fabricante.get()
        print(fabricante)
        marca = txt_marca.get()
        print(marca)
        cor = txt_cor.get()
        print(cor)
        fornecedor = Fornecedor.localiza_id_fornecedor(combo_fornecedor.get())
        print(fornecedor)
        data_cadastro = txt_data_cadastro.get()
        print(data_cadastro)

        
        
        produto = Produto(id, nome, preco_custo, tipo_produto_id, fabricante, marca, cor, fornecedor, data_cadastro)
        #produto.salvar_produto()
        if operacao == 'I':
            produto.salvar_produto()

            messagebox.showinfo("Cadastro", "Produto Cadastrado.")
        elif operacao == 'E':            
            produto.excluir_produto()                    
            messagebox.showinfo("Cadastro", "Produto excluído.")
        else:
            produto.alterar_produto()
            messagebox.showinfo("Cadastro", "Produto alterado.")
        carregar_produtos()        

        #messagebox.showinfo("Cadastro", "Produto inserido com sucesso.")

    
    #tk.Button(cadastro_janela, text="Salvar", command=salvar_produto).grid(row=9, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_produto('I')).grid(row=9, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_produto('A')).grid(row=9, columnspan=3, pady=10)
    #tk.Button(cadastro_janela, text="Excluir", command=lambda:salvar_produto('E')).grid(row=9, columnspan=4, pady=10)
    
    columns = ("ID", "Nome Produto", "Preço Custo", "Tipo", "Fabricante", "Marca", "Cor", "Fornecedor", "Data de Cadastro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Nome Produto", text="Nome Produto")
    treeview.heading("Preço Custo", text="Preço Custo")
    treeview.heading("Tipo", text="Tipo")
    treeview.heading("Fabricante", text="Fabricante")
    treeview.heading("Marca", text="Marca")
    treeview.heading("Cor", text="Cor")
    treeview.heading("Fornecedor", text="Fornecedor")
    treeview.heading("Data de Cadastro", text="Data de Cadastro")
    treeview.grid(row=10, column=0,columnspan=3, padx=10, pady=10)

    treeview.column("ID",width=30)
    treeview.column("Preço Custo",width=30)
    treeview.column("Cor",width=30)
    treeview.column("Marca",width=50)

    def carregar_produtos():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''SELECT A.ID_PRODUTO, A.NOME, A.PRECO_CUSTO, B.DESCRICAO, A.FABRICANTE,
                        A.MARCA, A.COR, C.NOME_EMPRESA, A.DATA_CADASTRO FROM TB_PRODUTO_NEW A
                        JOIN TB_TIPO_PRODUTO B ON B.COD = A.TIPO_PRODUTO
                        JOIN TB_FORNECEDOR C ON C.ID_FORNECEDOR = A.ID_FORNECEDOR;''')
        produtos = cursor.fetchall()

        # Adicionando os dados na Treeview
        for produto in produtos:
            treeview.insert("", "end", values=produto)
        
        conexao.close()
    
    # Carregar clientes ao abrir a janela
    carregar_produtos()

    #continuar aqui em 06/09/2024
    def ao_clicar_treeview_produto(event):
        item_selecionado = treeview.selection()

        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])

            txt_nome.delete(0,tk.END)
            txt_nome.insert(0,item[1])

            txt_preco_custo.delete(0,tk.END)
            txt_preco_custo.insert(0,item[2])

            combo_tipo_produto.set(item[3])

            txt_fabricante.delete(0,tk.END)
            txt_fabricante.insert(0,item[4])

            txt_marca.delete(0,tk.END)
            txt_marca.insert(0,item[5])
            
            txt_cor.delete(0,tk.END)
            txt_cor.insert(0,item[6])

            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[8])
            
            #ao_selecionar_combo_produto(event="<<ComboboxSelected>>")
    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get()
        #Nome', 'Marca', 'Tipo Produto', 'Fabricante','Cor','Fornecedor
        for item in treeview.get_children():
            treeview.delete(item)
        
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
                        A.MARCA, A.COR, C.NOME_EMPRESA, A.DATA_CADASTRO FROM TB_PRODUTO_NEW A
                        JOIN TB_TIPO_PRODUTO B ON B.COD = A.TIPO_PRODUTO
                        JOIN TB_FORNECEDOR C ON C.ID_FORNECEDOR = A.ID_FORNECEDOR
                        WHERE '''

        comando_final = comando + " " + condicao
        print(f'comando final: {comando_final}')
        print(f'filtro: {filtro}')
        
        cursor.execute(comando_final, ('%' + filtro + '%',))

        resultados = cursor.fetchall()
        
        for resultado in resultados:
            treeview.insert("", "end", values=resultado)

        conexao.close()
######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview_produto)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)

# fim tela cadastro produtos
######################################################################################

######################################################################################
#função para cadastro vendas
def cadastrar_venda():
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Venda")
    cadastro_janela.geometry("900x650")

    tk.Label(cadastro_janela, text="Data Venda").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="ID").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Cliente").grid(row=2, column=0, padx=10, pady=5, sticky="e")    
    tk.Label(cadastro_janela, text="Produto").grid(row=3, column=0, padx=10, pady=5, sticky="e") 
    tk.Label(cadastro_janela, text="Quantidade").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Preço Venda").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Lucro").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    lbl_filtrar =tk.Label(cadastro_janela, text="Filtrar")
    lbl_filtrar.grid(row=7, column=2, padx=0, pady=5, sticky="e")
    lbl_campo =tk.Label(cadastro_janela, text="Selecione:")
    lbl_campo.grid(row=6, column=2, padx=0, pady=5, sticky="e")                                    
    lbl_preco_sugerido = tk.Label(cadastro_janela, text="Preço sugerido: ")
    lbl_preco_sugerido.grid(row=5, column=2, padx=0, pady=5, sticky="w")

    txt_data_venda = tk.Entry(cadastro_janela)
    txt_data_venda.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    txt_data_venda.insert(0, datetime.now().strftime("%d/%m/%Y"))
    txt_id = tk.Entry(cadastro_janela)
    txt_id.grid(row=1, column=1, padx=9, pady=0, sticky="w")

    lista_clientes = Cliente.carregar_clientes_combo()
    combo_cliente = ttk.Combobox(cadastro_janela, values=lista_clientes)
    combo_cliente.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    lista_produtos = Produto.carregar_produtos_combo()
    combo_produto = ttk.Combobox(cadastro_janela, values=lista_produtos)
    combo_produto.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    lista_quantidade = ['1','2','3','4','5','6','7','8','9','10']
    txt_quantidade = ttk.Combobox(cadastro_janela, values=lista_quantidade)    
    txt_quantidade.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    txt_preco_venda = tk.Entry(cadastro_janela)
    txt_preco_venda.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    
    txt_lucro = tk.Entry(cadastro_janela)
    txt_lucro.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    
    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=7, column=3, padx=10, pady=5, sticky="w")

    lista_campos = ['Cliente', 'Produto', 'Fornecedor']
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos)
    combo_pesquisa.grid(row=6, column=3, padx=10, pady=5, sticky="w")
    
    
    def salvar_venda(operacao):
        id = int(txt_id.get())
        #cliente_id = fct.localiza_cliente_id(combo_cliente.get())
        #chamando pelo método da classe cliente
        cliente_id = Cliente.localiza_id_cliente(combo_cliente.get())
        produto_selecionado = combo_produto.get()
        partes = produto_selecionado.split('/')
        nome_produto = partes[0]
        nome_fornecedor = partes[-1]
        produto_id = Produto.localiza_produto_id(nome_produto,nome_fornecedor)        
        quantidade = int(txt_quantidade.get())
        preco_venda= txt_preco_venda.get()        
        data_venda = txt_data_venda.get()
        lucro = txt_lucro.get()        
        
        venda = Venda(id, data_venda, cliente_id, produto_id, quantidade, preco_venda, lucro)
        
        if operacao == 'I':
            venda.salvar_venda()        

            messagebox.showinfo("Cadastro", "A venda foi cadastrada.")
        elif operacao == 'E':            
            venda.excluir_venda()                    
            messagebox.showinfo("Cadastro", "A venda foi cadastrada.")
        else:
            venda.alterar_venda()

        carregar_vendas()
    
    

    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_venda('I')).grid(row=7, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_venda('A')).grid(row=7, columnspan=3, pady=10)
    tk.Button(cadastro_janela, text="Excluir", command=lambda:salvar_venda('E')).grid(row=7, columnspan=4, pady=10)

    def ao_selecionar_combo_produto(event):
        produto_selecionado = combo_produto.get()
        partes = produto_selecionado.split('/')
        nome_produto = partes[0]
        nome_fornecedor = partes[-1]
        #valor_sugerido = fct.calcular_preco_sugerido(nome_produto,nome_fornecedor)
        #chamar o preco sugerido através do método estático da classe venda
        valor_sugerido = Venda.calcular_preco_sugerido(nome_produto,nome_fornecedor)
        
        lbl_preco_sugerido.config(text=f'Preço sugerido: {valor_sugerido}')

    def ao_sair_preco_venda(event):
        preco_venda = float(txt_preco_venda.get())
        quantidade = txt_quantidade.get()
        str_preco_sugerido = lbl_preco_sugerido.cget('text')
        partes = str_preco_sugerido.split(':')
        valor_sugerido = float(partes[-1])
        if preco_venda > 0 and valor_sugerido > 0:
            lucro = (preco_venda - (valor_sugerido - 100)) * float(quantidade)
            txt_lucro.delete(0, tk.END)
            txt_lucro.insert(0,round(lucro,2))
        else:
            txt_lucro.insert(0,'falhou')


    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get()

        for item in treeview.get_children():
            treeview.delete(item)
        
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
                        join TB_PRODUTO_NEW c on a.ID_PRODUTO = c.ID_PRODUTO
                        join TB_FORNECEDOR d on c.ID_FORNECEDOR = d.ID_FORNECEDOR
                        WHERE'''

        comando_final = comando + " " + condicao
        #print(f'comando final: {comando_final}')
        #print(f'filtro: {filtro}')
        
        cursor.execute(comando_final, ('%' + filtro + '%',))

        resultados = cursor.fetchall()
        
        for resultado in resultados:
            treeview.insert("", "end", values=resultado)

        conexao.close()

    combo_produto.bind("<<ComboboxSelected>>", ao_selecionar_combo_produto)
    txt_preco_venda.bind("<FocusOut>", ao_sair_preco_venda)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)
    
    
    columns = ("ID", "Data", "Cliente", "Produto", "Quantidade", "Preço Venda", "Lucro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Data", text="Data")
    treeview.heading("Cliente", text="Cliente")
    treeview.heading("Produto", text="Produto")   
    treeview.heading("Quantidade", text="Quantidade")
    treeview.heading("Preço Venda", text="Preço Venda")
    treeview.heading("Lucro", text="Lucro")    
    treeview.grid(row=8, column=0,columnspan=4, padx=10, pady=10)

    treeview.column("ID",width=30)
    treeview.column("Preço Venda",width=80)
    treeview.column("Lucro",width=80)
    treeview.column("Quantidade",width=30)
    #treeview.column("Cor",width=30)
    #treeview.column("Marca",width=50)
    

    def carregar_vendas():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''select a.id, a.DATA, b.NOME, c.NOME || '/' || c.MARCA || '/'|| d.NOME_EMPRESA as Produto, a.QUANTIDADE, a.PRECO_VENDA, a.LUCRO
                        from TB_VENDA a
                        join TB_CLIENTE b on a.ID_CLIENTE = b.ID_CLIENTE
                        join TB_PRODUTO_NEW c on a.ID_PRODUTO = c.ID_PRODUTO
                        join TB_FORNECEDOR d on c.ID_FORNECEDOR = d.ID_FORNECEDOR;''')
        vendas = cursor.fetchall()

        # Adicionando os dados na Treeview
        for venda in vendas:
            treeview.insert("", "end", values=venda)
        
        conexao.close()
    
    # Carregar clientes ao abrir a janela
    carregar_vendas()

######################################################################################

######################################################################################
#lidar com prenchimento caixas após clique na treeview
    def ao_clicar_treeview(event):
        item_selecionado = treeview.selection()

        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])

            txt_data_venda.delete(0,tk.END)
            txt_data_venda.insert(0,item[1])

            combo_cliente.set(item[2])

            combo_produto.set(item[3])

            txt_quantidade.set(item[4])

            txt_preco_venda.delete(0,tk.END)
            txt_preco_venda.insert(0,item[5])

            txt_lucro.delete(0,tk.END)
            txt_lucro.insert(0,item[6])
            
            ao_selecionar_combo_produto(event="<<ComboboxSelected>>")

######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)

# Criação da janela principal
root = tk.Tk()
root.title("GTECH IMPORTS")
root.geometry("600x400")

# Criação da label principal
label = tk.Label(root, text="GTECH IMPORTS", font=("Arial", 16))
label.pack(pady=10)

# Criação do menu inicial
menu_barra = tk.Menu(root)

menu_cliente = tk.Menu(menu_barra,tearoff=0)
menu_cliente.add_command(label="Cadastro",command=lambda:cadastrar_cliente(root))
menu_barra.add_cascade(label="Cliente",menu=menu_cliente)

menu_fornecedor = tk.Menu(menu_barra,tearoff=0)
menu_fornecedor.add_command(label="Cadastro",command=cadastrar_fornecedor)
menu_barra.add_cascade(label="Fornecedor",menu=menu_fornecedor)


menu_produto = tk.Menu(menu_barra,tearoff=0)
menu_produto.add_command(label="Cadastro", command=cadastrar_produto)
menu_produto.add_command(label="Tipo de Produto", command=cadastrar_tipo_produto)
menu_produto.add_separator()
menu_barra.add_cascade(label="Produto",menu=menu_produto)

menu_venda = tk.Menu(menu_barra,tearoff=0)
menu_venda.add_command(label="Cadastro", command=cadastrar_venda)
menu_barra.add_cascade(label="Venda", menu=menu_venda)

root.config(menu=menu_barra)

######################################################################
#inserir a logo da empresa na tela inicial
#logo_empresa = PhotoImage(file="C:/Users/amilt/OneDrive/Documentos/PROJETO GTECH/PROJETO/projeto_gtech/midia/gtech_logo.png")
#label_logo = tk.Label(root,image=logo_empresa)
#label_logo.pack(pady=0)

# Obter o caminho absoluto do diretório do programa
diretorio_programa = os.path.dirname(os.path.abspath(__file__))

# Construir o caminho completo para a imagem dentro da pasta "midia"
caminho_imagem = os.path.join(diretorio_programa, "midia", "gtech_logo.png")

# Carregar a imagem da logo
logo = PhotoImage(file=caminho_imagem)

# Inserir a imagem no centro da tela
label_logo = tk.Label(root, image=logo)
label_logo.image = logo  # Manter referência para evitar garbage collection
label_logo.pack(pady=20)




# Inicia o loop principal da interface
root.mainloop()
