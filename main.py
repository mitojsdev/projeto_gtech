import funcoes as fct
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
#from funcoes import localiza_tipo_produto, localiza_id_fornecedor, localiza_cliente_id, localiza_produto_id
valor_sugerido = 0

import os



# Função para abrir a tela de cadastro de cliente
def cadastrar_cliente():
    # Nova janela para cadastro de cliente
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Cliente")
    cadastro_janela.geometry("850x450")

    # Campos de entrada
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Telefone").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Data de Cadastro").grid(row=3, column=0, padx=10, pady=5, sticky="e")

    txt_id = tk.Entry(cadastro_janela)
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome = tk.Entry(cadastro_janela)
    txt_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    txt_telefone = tk.Entry(cadastro_janela)
    txt_telefone.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    # Função para salvar o cliente
    def salvar_cliente():
        id_cliente = int(txt_id.get())
        nome = txt_nome.get()
        telefone = txt_telefone.get()
        data_cadastro = txt_data_cadastro.get()

        # Instanciando a classe Cliente
        cliente = Cliente(id_cliente, nome, telefone, data_cadastro)
        cliente.salvar_no_banco()
        # Adicionando o cliente à treeview
        #treeview.insert("", "end", values=(id_cliente, nome, telefone, data_cadastro))

        messagebox.showinfo("Cadastro", "Cliente inserido com sucesso.")

    # Botão para salvar o cliente
    tk.Button(cadastro_janela, text="Salvar Cliente", command=salvar_cliente).grid(row=4, columnspan=2, pady=10)

    # Criando a Treeview para exibir os clientes cadastrados
    columns = ("ID", "Nome", "Telefone", "Data de Cadastro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Nome", text="Nome")
    treeview.heading("Telefone", text="Telefone")
    treeview.heading("Data de Cadastro", text="Data de Cadastro")
    treeview.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def carregar_clientes():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM TB_CLIENTE")
        clientes = cursor.fetchall()

        # Adicionando os dados na Treeview
        for cliente in clientes:
            treeview.insert("", "end", values=cliente)
        
        conexao.close()

    # Carregar clientes ao abrir a janela
    carregar_clientes()


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

    
    def salvar_fornecedor():
        id = int(txt_id.get())
        nome = txt_nome_empresa.get()
        tipo_empresa = combo_tipo_empresa.get()
        data_cadastro = txt_data_cadastro.get()

        
        fornecedor = Fornecedor(id, nome, tipo_empresa, data_cadastro)
        fornecedor.salvar_no_banco()        

        messagebox.showinfo("Cadastro", "Fornecedor inserido com sucesso.")

    
    tk.Button(cadastro_janela, text="Salvar", command=salvar_fornecedor).grid(row=4, columnspan=2, pady=10)

    
    columns = ("ID", "Nome Empresa", "Tipo Empresa", "Data de Cadastro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Nome Empresa", text="Nome Empresa")
    treeview.heading("Tipo Empresa", text="Tipo Empresa")
    treeview.heading("Data de Cadastro", text="Data de Cadastro")
    treeview.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

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
    
    def salvar_produto():
        id = int(txt_id.get())
        print(id)
        nome = txt_nome.get()
        print(nome)
        preco_custo = float(txt_preco_custo.get())
        print(preco_custo)
        tipo_produto = combo_tipo_produto.get()        
        tipo_produto_id = fct.localiza_produto_idlocaliza_tipo_produto(tipo_produto)
        print(tipo_produto_id)
        print(type(tipo_produto_id))
        fabricante = txt_fabricante.get()
        print(fabricante)
        marca = txt_marca.get()
        print(marca)
        cor = txt_cor.get()
        print(cor)
        fornecedor = fct.localiza_id_fornecedor(combo_fornecedor.get())
        print(fornecedor)
        data_cadastro = txt_data_cadastro.get()
        print(data_cadastro)

        
        produto = Produto(id, nome, preco_custo, tipo_produto_id, fabricante, marca, cor, fornecedor, data_cadastro)
        produto.salvar_produto()        

        messagebox.showinfo("Cadastro", "Produto inserido com sucesso.")

    
    tk.Button(cadastro_janela, text="Salvar", command=salvar_produto).grid(row=10, columnspan=2, pady=10)

    
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
    treeview.grid(row=9, column=0,columnspan=2, padx=10, pady=10)

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
        cursor.execute("SELECT * FROM TB_PRODUTO_NEW")
        produtos = cursor.fetchall()

        # Adicionando os dados na Treeview
        for produto in produtos:
            treeview.insert("", "end", values=produto)
        
        conexao.close()
    
    # Carregar clientes ao abrir a janela
    carregar_produtos()

######################################################################################

######################################################################################
#função para cadastrar vendas
def cadastrar_venda():
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Venda")
    cadastro_janela.geometry("1200x650")

    tk.Label(cadastro_janela, text="Data Venda").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="ID").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Cliente").grid(row=2, column=0, padx=10, pady=5, sticky="e")    
    tk.Label(cadastro_janela, text="Produto").grid(row=3, column=0, padx=10, pady=5, sticky="e") 
    tk.Label(cadastro_janela, text="Quantidade").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Preço Venda").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Lucro").grid(row=6, column=0, padx=10, pady=5, sticky="e")         
    lbl_preco_sugerido = tk.Label(cadastro_janela, text="Preço sugerido: ")
    lbl_preco_sugerido.grid(row=5, column=2, padx=10, pady=5, sticky="e")
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
    
    
    
    def salvar_venda():
        id = int(txt_id.get())
        cliente_id = fct.localiza_cliente_id(combo_cliente.get())
        produto_id = fct.localiza_produto_id(combo_produto.get())        
        quantidade = int(txt_quantidade.get())
        preco_venda= float(txt_preco_venda.get())
        #lucro = float(txt_lucro.get())        
        data_venda = txt_data_venda.get()        
        
        venda = Venda(id, data_venda, cliente_id, produto_id, quantidade, preco_venda, lucro)
        venda.salvar_venda()        

        messagebox.showinfo("Cadastro", "A venda foi cadastrada.")

    

    tk.Button(cadastro_janela, text="Salvar", command=salvar_venda).grid(row=7, columnspan=2, pady=10)

    def ao_selecionar_combo_produto(event):
        produto_selecionado = combo_produto.get()
        partes = produto_selecionado.split('/')
        nome_produto = partes[0]
        nome_fornecedor = partes[-1]
        valor_sugerido = fct.calcular_preco_sugerido(nome_produto,nome_fornecedor)
        lbl_preco_sugerido.config(text=f'Preço sugerido: {valor_sugerido}')

    def ao_sair_preco_venda(event):
        preco_venda = float(txt_preco_venda.get())
        str_preco_sugerido = lbl_preco_sugerido.cget('text')
        partes = str_preco_sugerido.split(':')
        valor_sugerido = float(partes[-1])
        if preco_venda > 0 and valor_sugerido > 0:
            lucro = preco_venda - (valor_sugerido - 100)
            txt_lucro.delete(0, tk.END)
            txt_lucro.insert(0,round(lucro,2))
        else:
            txt_lucro.insert(0,'falhou')

    combo_produto.bind("<<ComboboxSelected>>", ao_selecionar_combo_produto)
    txt_preco_venda.bind("<FocusOut>", ao_sair_preco_venda)
   
    #columns = ("ID", "Nome Produto", "Preço Custo", "Tipo", "Fabricante", "Marca", "Cor", "Fornecedor", "Data de Cadastro")
    #treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    #treeview.heading("ID", text="ID")
    #treeview.heading("Nome Produto", text="Nome Produto")
    #treeview.heading("Preço Custo", text="Preço Custo")
    #treeview.heading("Tipo", text="Tipo")
    #treeview.heading("Fabricante", text="Fabricante")
    #treeview.heading("Marca", text="Marca")
    #treeview.heading("Cor", text="Cor")
    #treeview.heading("Fornecedor", text="Fornecedor")
    #treeview.heading("Data de Cadastro", text="Data de Cadastro")
    #treeview.grid(row=9, column=0,columnspan=2, padx=10, pady=10)

    #treeview.column("ID",width=30)
    #treeview.column("Preço Custo",width=30)
    #treeview.column("Cor",width=30)
    #treeview.column("Marca",width=50)

    #def carregar_produtos():
        # Limpa a Treeview antes de carregar os dados
        #for item in treeview.get_children():
         #   treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados
        #conexao = conectar()
        #cursor = conexao.cursor()
        #cursor.execute("SELECT * FROM TB_PRODUTO_NEW")
        #produtos = cursor.fetchall()

        # Adicionando os dados na Treeview
        #for produto in produtos:
         #   treeview.insert("", "end", values=produto)
        
        #conexao.close()
    
    # Carregar clientes ao abrir a janela
    #carregar_produtos()

######################################################################################

    
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
menu_cliente.add_command(label="Cadastro",command=cadastrar_cliente)
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
