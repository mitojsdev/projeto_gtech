import tkinter as tk
from tkinter import ttk
from datetime import datetime
from modelos import Cliente


def cadastrar_cliente(root):
    # Nova janela para cadastro de cliente
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Cliente")
    cadastro_janela.geometry("850x450")

    # Campos de entrada
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Telefone").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Data de Cadastro").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    lbl_filtrar =tk.Label(cadastro_janela, text="Filtrar")
    lbl_filtrar.grid(row=4, column=1, padx=0, pady=5, sticky="e")
    lbl_campo =tk.Label(cadastro_janela, text="Selecione:")
    lbl_campo.grid(row=3, column=1, padx=0, pady=5, sticky="e")

    txt_id = tk.Entry(cadastro_janela)
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome = tk.Entry(cadastro_janela)
    txt_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    txt_telefone = tk.Entry(cadastro_janela)
    txt_telefone.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    lista_campos = ['Nome',]
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos)
    combo_pesquisa.grid(row=3, column=2, padx=10, pady=5, sticky="w")

    # Função para salvar o cliente
    def salvar_cliente(operacao):
        id_cliente = int(txt_id.get())
        nome = txt_nome.get()
        telefone = txt_telefone.get()
        data_cadastro = txt_data_cadastro.get()

        # Instanciando a classe Cliente
        cliente = Cliente(id_cliente, nome, telefone, data_cadastro)
        
        if operacao == 'I':
            cliente.salvar_cliente()            
        else:
            cliente.alterar_cliente()            
                
        carregar_clientes()
        

    # Botão para salvar o cliente
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_cliente('I')).grid(row=4, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_cliente('A')).grid(row=4, columnspan=3, pady=10)



    # Criando a Treeview para exibir os clientes cadastrados
    columns = ("ID", "Nome", "Telefone", "Data de Cadastro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Nome", text="Nome")
    treeview.heading("Telefone", text="Telefone")
    treeview.heading("Data de Cadastro", text="Data de Cadastro")
    treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def carregar_clientes():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)
       
        clientes = Cliente.carregar_clientes_treeview()

        # Adicionando os dados na Treeview
        for cliente in clientes:
            treeview.insert("", "end", values=cliente)               

    def ao_clicar_treeview(event):
        item_selecionado = treeview.selection()
        #id, nome, telefone, data_cad
        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])

            txt_nome.delete(0,tk.END)
            txt_nome.insert(0,item[1])

            txt_telefone.delete(0,tk.END)
            txt_telefone.insert(0,item[2])
            
            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[3])
                        
    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get()
        #Nome,
        for item in treeview.get_children():
            treeview.delete(item)

        resultados = Cliente.pesquisa_clientes(campo, filtro)
        
        for resultado in resultados:
            treeview.insert("", "end", values=resultado)

    # Carregar clientes ao abrir a janela
    carregar_clientes()
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)