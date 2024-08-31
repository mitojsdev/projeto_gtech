import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from modelos import Cliente  # Importando a Classe Cliente
from conexao import conectar

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

# Funções dos botões da tela principal
def cadastrar_produto():
    print("Cadastrar Produto")

def cadastrar_venda():
    print("Cadastrar Venda")

# Criação da janela principal
root = tk.Tk()
root.title("GTECH IMPORTS")
root.geometry("300x200")

# Criação da label principal
label = tk.Label(root, text="GTECH IMPORTS", font=("Arial", 16))
label.pack(pady=10)

# Criação dos botões
btn_produto = tk.Button(root, text="CADASTRAR PRODUTO", command=cadastrar_produto)
btn_produto.pack(pady=5)

btn_venda = tk.Button(root, text="CADASTRAR VENDA", command=cadastrar_venda)
btn_venda.pack(pady=5)

btn_cliente = tk.Button(root, text="CADASTRAR CLIENTE", command=cadastrar_cliente)
btn_cliente.pack(pady=5)

# Inicia o loop principal da interface
root.mainloop()
