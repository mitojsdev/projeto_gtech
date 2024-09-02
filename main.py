import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from modelos import Cliente  # Importando a Classe Cliente
from modelos import TipoProduto
from conexao import conectar
from tkinter import PhotoImage
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


# Funções dos botões da tela principal
def cadastrar_produto():
    print("Cadastrar Produto")

def cadastrar_venda():
    print("Cadastrar Venda")

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

menu_produto = tk.Menu(menu_barra,tearoff=0)
menu_produto.add_command(label="Cadastro")
menu_produto.add_command(label="Tipo de Produto", command=cadastrar_tipo_produto)
menu_produto.add_separator()
menu_barra.add_cascade(label="Produto",menu=menu_produto)

menu_venda = tk.Menu(menu_barra,tearoff=0)
menu_venda.add_command(label="Cadastro")
menu_barra.add_cascade(label="Venda", menu=menu_venda)

root.config(menu=menu_barra)

######################################################################
#inserir a logo da empresa na tela inicial
logo_empresa = PhotoImage(file="C:/Users/amilt/OneDrive/Documentos/PROJETO GTECH/PROJETO/projeto_gtech/midia/gtech_logo.png")
label_logo = tk.Label(root,image=logo_empresa)
label_logo.pack(pady=0)




# Inicia o loop principal da interface
root.mainloop()
