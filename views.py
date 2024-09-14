import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from modelos import Cliente, Fornecedor, TipoProduto, Produto, Venda
from funcoes import valida_campo


def cadastrar_cliente(root):
    # Nova janela para cadastro de cliente
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
    #odal_window.grab_set()
    cadastro_janela.title("Cadastro de Cliente")
    cadastro_janela.geometry("700x450")



    # Campos de entrada
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Telefone").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Data de Cadastro").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    lbl_filtrar =tk.Label(cadastro_janela, text="Filtrar")
    lbl_filtrar.grid(row=4, column=1, padx=0, pady=5, sticky="e")
    lbl_campo =tk.Label(cadastro_janela, text="Selecione:")
    lbl_campo.grid(row=3, column=1, padx=0, pady=5, sticky="e")


    # Criando um Entry
    #entry = tk.Entry(root, state='disabled', disabledbackground='lightgrey', disabledforeground='darkgrey')
    #entry.pack()
    txt_id = tk.Entry(cadastro_janela,state='disabled', disabledbackground='lightgrey',disabledforeground='darkgrey')    
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome = tk.Entry(cadastro_janela,width=50)
    txt_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    txt_telefone = tk.Entry(cadastro_janela)
    txt_telefone.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    lista_campos = ['Nome',]
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos,state="readonly")
    combo_pesquisa.grid(row=3, column=2, padx=10, pady=5, sticky="w")

    lista_entradas = [txt_id,txt_nome,txt_telefone]

    def limpar_campos():
    # Limpar todas as caixas de entrada
        for entry in lista_entradas:
            if entry == txt_id: 
                entry.config(state='normal')
                entry.delete(0, tk.END)  
                entry.config(state='disabled')
            else:
                entry.delete(0, tk.END)
        txt_nome.focus()

    # Função para salvar/alterar o cliente
    def salvar_cliente(operacao):               
        if not valida_campo('nome', txt_nome.get()):
            form = False
        elif not valida_campo('telefone', txt_telefone.get()):
            form = False
        elif not valida_campo('data', txt_data_cadastro.get()):
            form = False
        else:
            form = True
  
        if form:            
            nome = txt_nome.get().upper()
            telefone = txt_telefone.get()
            data_cadastro = txt_data_cadastro.get()
            if operacao == 'I':                        
                # Instanciando a classe Cliente
                cliente = Cliente(nome, telefone, data_cadastro)
                cliente.salvar_cliente()
                limpar_campos()             
            else:
                if valida_campo('id',txt_id.get()):
                    id_cliente = int(txt_id.get())
                    cliente = Cliente(nome, telefone, data_cadastro, id_cliente)
                    cliente.alterar_cliente()
                    limpar_campos()
        carregar_clientes()
        

    # Botão para salvar o cliente
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_cliente('I')).grid(row=4, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_cliente('A')).grid(row=4, columnspan=3, pady=10)


    # Criando a Treeview para exibir os clientes cadastrados
    columns = ("ID", "Nome", "Telefone", "Data de Cadastro")
    frame_treeview = ttk.Frame(cadastro_janela)
    frame_treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    treeview = ttk.Treeview(frame_treeview, columns=columns, show="headings")
    treeview.heading("ID", text="ID", anchor='w')
    treeview.heading("Nome", text="Nome", anchor='w')
    treeview.heading("Telefone", text="Telefone", anchor='w')
    treeview.heading("Data de Cadastro", text="Data de Cadastro", anchor='w')

    # Configurando a barra de rolagem
    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)

    # Posicionando a Treeview e a Scrollbar
    treeview.pack(side=tk.LEFT)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    treeview.column("ID", width=30)
    treeview.column("Data de Cadastro", width=100)
    

    def carregar_clientes():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)
       
        clientes = Cliente.carregar_clientes_treeview()
        
        # Adicionando os dados na Treeview
        for cliente in clientes:
            data_original = cliente[3]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            cliente_lista = list(cliente)
            cliente_lista[3] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(cliente_lista))

    def ao_clicar_treeview(event):
        item_selecionado = treeview.selection()
        #id, nome, telefone, data_cad
        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.config(state='normal')
            txt_id.delete(0,tk.END)                        
            txt_id.insert(0,item[0])
            txt_id.config(state='disabled')

            txt_nome.delete(0,tk.END)
            txt_nome.insert(0,item[1])

            txt_telefone.delete(0,tk.END)
            txt_telefone.insert(0,item[2])
            
            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[3])

                        
    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get().upper()
        #Nome,
        for item in treeview.get_children():
            treeview.delete(item)

        resultados = Cliente.pesquisa_clientes(campo, filtro)
        
        for resultado in resultados:
            data_original = resultado[3]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            resultado_lista = list(resultado)
            resultado_lista[3] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(resultado_lista))            

    # Carregar clientes ao abrir a janela
    carregar_clientes()
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)



    ##############################################################################

    ######################################################################################
#função para cadastrar fornecedor
def cadastrar_fornecedor(root):
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
    cadastro_janela.title("Cadastro de Fornecedor")
    cadastro_janela.geometry("650x450")

    
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome Empresa").grid(row=1, column=0, padx=10, pady=5, sticky="e")    
    tk.Label(cadastro_janela, text="Tipo Empresa").grid(row=2, column=0, padx=10, pady=5, sticky="e") 
    tk.Label(cadastro_janela, text="Data Cadastro").grid(row=3, column=0, padx=10, pady=5, sticky="e") 
    lbl_filtrar =tk.Label(cadastro_janela, text="Filtrar")
    lbl_filtrar.grid(row=4, column=1, padx=0, pady=5, sticky="e")
    lbl_campo =tk.Label(cadastro_janela, text="Selecione:")
    lbl_campo.grid(row=3, column=1, padx=0, pady=5, sticky="e")

    txt_id = tk.Entry(cadastro_janela,state='disabled', disabledbackground='lightgrey',disabledforeground='darkgrey')
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome_empresa = tk.Entry(cadastro_janela,width=50)
    txt_nome_empresa.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tipos_empresa = ['Física', 'Virtual', 'Outro']    
    combo_tipo_empresa = ttk.Combobox(cadastro_janela, values=tipos_empresa, state='readonly')
    combo_tipo_empresa.current(0)
    combo_tipo_empresa.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    lista_campos = ['Nome', 'Tipo Empresa']
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos, state='readonly')
    combo_pesquisa.grid(row=3, column=2, padx=10, pady=5, sticky="w")
    
    lista_entradas = [txt_id,txt_nome_empresa]    

    def limpar_campos():
        # Limpar todas as caixas de entrada
        for entry in lista_entradas:
            if entry == txt_id: 
                entry.config(state='normal')
                entry.delete(0, tk.END)  
                entry.config(state='disabled')
            else:
                entry.delete(0, tk.END)

        combo_tipo_empresa.set('')

        txt_nome_empresa.focus()


    def salvar_fornecedor(operacao):
        if not valida_campo('nome', txt_nome_empresa.get()):
            form = False
        elif not valida_campo('tipo_empresa', combo_tipo_empresa.get()):
            form = False
        elif not valida_campo('data', txt_data_cadastro.get()):
            form = False
        else:
            form = True

        if form:            
            nome = txt_nome_empresa.get().upper()
            tipo_empresa = combo_tipo_empresa.get().upper()
            data_cadastro = txt_data_cadastro.get()
            if operacao == 'I':                        
                # Instanciando a classe Fornecedor
                fornecedor = Fornecedor(nome, tipo_empresa, data_cadastro)
                fornecedor.salvar_fornecedor()
                limpar_campos()             
            else:
                if valida_campo('id',txt_id.get()):
                    id_fornecedor = int(txt_id.get())
                    fornecedor = Fornecedor(nome, tipo_empresa, data_cadastro, id_fornecedor)
                    fornecedor.alterar_fornecedor()
                    limpar_campos()

        carregar_fornecedores()
    
    #tk.Button(cadastro_janela, text="Salvar", command=salvar_fornecedor).grid(row=4, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_fornecedor('I')).grid(row=4, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_fornecedor('A')).grid(row=4, columnspan=3, pady=10)
    
    # Criando a Treeview para exibir fornecedores cadastrados
    columns = ("ID", "Nome Empresa", "Tipo Empresa", "Data de Cadastro")
    frame_treeview = ttk.Frame(cadastro_janela)
    frame_treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    treeview = ttk.Treeview(frame_treeview, columns=columns, show="headings")
    treeview.heading("ID", text="ID", anchor='w')
    treeview.heading("Nome Empresa", text="Nome Empresa", anchor='w')
    treeview.heading("Tipo Empresa", text="Tipo Empresa", anchor='w')
    treeview.heading("Data de Cadastro", text="Data de Cadastro", anchor='w')

    # Configurando a barra de rolagem
    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)

    # Posicionando a Treeview e a Scrollbar
    treeview.pack(side=tk.LEFT)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Definindo a largura das colunas
    treeview.column("ID", width=30)
    treeview.column("Data de Cadastro", width=100)

    def carregar_fornecedores():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)
        
        fornecedores = Fornecedor.carregar_fornecedores_treeview()

        # Adicionando os dados na Treeview
        for fornecedor in fornecedores:
            data_original = fornecedor[3]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            fornecedor_lista = list(fornecedor)
            fornecedor_lista[3] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(fornecedor_lista))

            
    carregar_fornecedores()
    
    def ao_clicar_treeview(event):
        item_selecionado = treeview.selection()

        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.config(state='normal')
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])
            txt_id.config(state='disabled')

            txt_nome_empresa.delete(0,tk.END)
            txt_nome_empresa.insert(0,item[1])

            combo_tipo_empresa.set(item[2])
            
            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[3])

    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get().upper()
        
        for item in treeview.get_children():
            treeview.delete(item)
        
        resultados = Fornecedor.pesquisa_fornecedor(campo, filtro)
        
        for resultado in resultados:
            data_original = resultado[3]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            resultado_lista = list(resultado)
            resultado_lista[3] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(resultado_lista))
        
######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)

######################################################################################

#tela produto
######################################################################################
def cadastrar_produto(root):
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
    cadastro_janela.title("Cadastro de Produto")
    cadastro_janela.geometry("1200x650")

    
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Nome").grid(row=1, column=0, padx=10, pady=5, sticky="e")    
    tk.Label(cadastro_janela, text="Preço Custo").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Estoque").grid(row=2, column=1, padx=200, pady=5, sticky="w")
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


    txt_id = tk.Entry(cadastro_janela,state='disabled', disabledbackground='lightgrey',disabledforeground='darkgrey')
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome = tk.Entry(cadastro_janela,width=50)
    txt_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    txt_preco_custo = tk.Entry(cadastro_janela)
    txt_preco_custo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    lista_estoque = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    combo_estoque = ttk.Combobox(cadastro_janela, values=lista_estoque,width=5, state='readonly')
    combo_estoque.current(0)
    combo_estoque.grid(row=2, column=1, padx=270, pady=5, sticky="w")    

    tipos_produto = TipoProduto.carregar_tipos_produto()    
    combo_tipo_produto = ttk.Combobox(cadastro_janela, values=tipos_produto, state='readonly')
    combo_tipo_produto.current(0)
    combo_tipo_produto.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    txt_fabricante = tk.Entry(cadastro_janela)
    txt_fabricante.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    
    txt_marca = tk.Entry(cadastro_janela)
    txt_marca.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    txt_cor = tk.Entry(cadastro_janela)
    txt_cor.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    lista_fornecedores = Fornecedor.carregar_fornecedores_combo()
    combo_fornecedor = ttk.Combobox(cadastro_janela, values=lista_fornecedores, width=50, state='readonly')
    combo_fornecedor.current(0)
    combo_fornecedor.grid(row=7, column=1, padx=10, pady=5, sticky="w")

    txt_data_cadastro = tk.Entry(cadastro_janela)
    txt_data_cadastro.grid(row=8, column=1, padx=10, pady=5, sticky="w")
    txt_data_cadastro.insert(0, datetime.now().strftime("%d/%m/%Y"))

    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=9, column=2, padx=10, pady=5, sticky="w")

    lista_campos = ['Nome', 'Marca', 'Tipo Produto', 'Fabricante','Cor','Fornecedor']
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos, state='readonly')
    combo_pesquisa.grid(row=8, column=2, padx=10, pady=5, sticky="w")
    
    def salvar_produto(operacao):        
        if not valida_campo('nome', txt_nome.get()):
            form = False
        elif not valida_campo('moeda', txt_preco_custo.get()) or not valida_campo('Preço Custo',txt_preco_custo.get()):
            form = False
        elif not valida_campo('tipo_produto', combo_tipo_produto.get()):
            form = False
        elif not valida_campo('fabricante', txt_fabricante.get()):
            form = False
        elif not valida_campo('marca', txt_marca.get()):
            form = False
        elif not valida_campo('cor', txt_cor.get()):
            form = False
        elif not valida_campo('fornecedor', combo_fornecedor.get()):
            form = False
        elif not valida_campo('data', txt_data_cadastro.get()):
            form = False
        elif not valida_campo('estoque', combo_estoque.get()):
            form = False
        elif not valida_campo('Nome_Produto', txt_nome.get()):
            form = False
        else:
            form = True

        if form:        
            nome = txt_nome.get().upper()                        
            preco_custo = float(txt_preco_custo.get().replace(',','.'))            
            tipo_produto = combo_tipo_produto.get()                
            tipo_produto_id = TipoProduto.localiza_tipo_produto(tipo_produto)            
            fabricante = txt_fabricante.get().upper()
            marca = txt_marca.get().upper()            
            cor = txt_cor.get().upper()            
            fornecedor = Fornecedor.localiza_id_fornecedor(combo_fornecedor.get())            
            data_cadastro = txt_data_cadastro.get()
            estoque = int(combo_estoque.get())
        
            if operacao == 'I':
                produto = Produto(nome, preco_custo, tipo_produto_id, fabricante, marca, cor, fornecedor, data_cadastro, estoque)
                produto.salvar_produto()
                limpar_campos()
            else:
                if valida_campo('id', txt_id.get()):
                    id_produto = txt_id.get()
                    produto = Produto(nome, preco_custo, tipo_produto_id, fabricante, marca, cor, fornecedor, data_cadastro, estoque, id_produto)
                    produto.alterar_produto()
                    limpar_campos()
        carregar_produtos()        
               
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_produto('I')).grid(row=9, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_produto('A')).grid(row=9, columnspan=3, pady=10)
    
    
    columns = ("ID", "Nome Produto", "Preço Custo", "Tipo", "Fabricante", "Marca", "Cor", "Fornecedor", "Data de Cadastro", "Estoque")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    #treeview.grid(row=10, column=0,columnspan=4, padx=10, pady=10)
    treeview.heading("ID", text="ID", anchor='w')
    treeview.heading("Nome Produto", text="Nome Produto", anchor='w')
    treeview.heading("Preço Custo", text="Preço Custo", anchor='w')
    treeview.heading("Tipo", text="Tipo", anchor='w')
    treeview.heading("Fabricante", text="Fabricante", anchor='w')
    treeview.heading("Marca", text="Marca", anchor='w')
    treeview.heading("Cor", text="Cor", anchor='w')
    treeview.heading("Fornecedor", text="Fornecedor", anchor='w')
    treeview.heading("Data de Cadastro", text="Data de Cadastro", anchor='w')
    treeview.heading("Estoque", text="Estoque", anchor='w')

    scrollbar = ttk.Scrollbar(cadastro_janela, orient="vertical", command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)

    treeview.grid(row=10, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    scrollbar.grid(row=10, column=4, sticky='ns')
    

    treeview.column("ID",width=30)
    treeview.column("Estoque",width=80)
    treeview.column("Preço Custo",width=80)
    treeview.column("Cor",width=60)
    treeview.column("Marca",width=60)
    treeview.column('Tipo', width=80)

    def carregar_produtos():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)                
            
        produtos = Produto.carregar_produtos_treeview()
            
        
        # Adicionando os dados na Treeview
        for produto in produtos:
            data_original = produto[8]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            produto_lista = list(produto)
            produto_lista[8] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(produto_lista))
        
        
    
    # Carregar clientes ao abrir a janela
    carregar_produtos()

    #continuar aqui em 06/09/2024
    def ao_clicar_treeview_produto(event):
        item_selecionado = treeview.selection()

        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')            
            txt_id.config(state='normal')
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])
            txt_id.config(state='disabled')

            txt_nome.delete(0,tk.END)
            txt_nome.insert(0,item[1])

            txt_preco_custo.delete(0,tk.END)
            txt_preco_custo.insert(0,item[2].replace('.',','))            

            combo_tipo_produto.set(item[3])

            txt_fabricante.delete(0,tk.END)
            txt_fabricante.insert(0,item[4])

            txt_marca.delete(0,tk.END)
            txt_marca.insert(0,item[5])
            
            txt_cor.delete(0,tk.END)
            txt_cor.insert(0,item[6])

            combo_fornecedor.set(item[7])

            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[8])
            
            combo_estoque.set(item[9])
            #ao_selecionar_combo_produto(event="<<ComboboxSelected>>")
    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get().upper()
        
        for item in treeview.get_children():
            treeview.delete(item)

        resultados = Produto.pesquisar_produtos(campo,filtro)
        
        for resultado in resultados:
            data_original = resultado[8]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            resultado_lista = list(resultado)
            resultado_lista[8] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(resultado_lista))
    
    lista_entradas = [txt_id, txt_nome, txt_marca, txt_fabricante, txt_cor, txt_preco_custo]
    def limpar_campos():
        for entry in (lista_entradas):
            if entry == txt_id: 
                entry.config(state='normal')
                entry.delete(0, tk.END)  
                entry.config(state='disabled')
            else:
                entry.delete(0, tk.END)
        combo_fornecedor.set('')
        combo_tipo_produto.set('')
        combo_estoque.set('')

        txt_nome.focus()
        
######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview_produto)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)

# fim tela cadastro produtos
######################################################################################


######################################################################################
#função para cadastro vendas
def cadastrar_venda(root):
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
    cadastro_janela.title("Cadastro de Venda")
    cadastro_janela.geometry("820x650")

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
    lbl_preco_sugerido.grid(row=5, column=1, padx=80, pady=5, sticky="e")

    txt_data_venda = tk.Entry(cadastro_janela)
    txt_data_venda.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    txt_data_venda.insert(0, datetime.now().strftime("%d/%m/%Y"))
    txt_id = tk.Entry(cadastro_janela, state='disabled',disabledbackground='lightgrey',disabledforeground='darkgrey')
    txt_id.grid(row=1, column=1, padx=9, pady=0, sticky="w")

    lista_clientes = Cliente.carregar_clientes_combo()
    combo_cliente = ttk.Combobox(cadastro_janela, values=lista_clientes, width=50, state='readonly')
    combo_cliente.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    lista_produtos = Produto.carregar_produtos_combo()
    combo_produto = ttk.Combobox(cadastro_janela, values=lista_produtos, width=50, state='readonly')
    combo_produto.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    lista_quantidade = ['1','2','3','4','5','6','7','8','9','10']
    txt_quantidade = ttk.Combobox(cadastro_janela, values=lista_quantidade, width=5, state='readonly')    
    txt_quantidade.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    txt_preco_venda = tk.Entry(cadastro_janela)
    txt_preco_venda.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    
    txt_lucro = tk.Entry(cadastro_janela, state='disabled')    
    txt_lucro.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    
    txt_pesquisa = tk.Entry(cadastro_janela, width=30)
    txt_pesquisa.grid(row=7, column=3, padx=10, pady=5, sticky="w")

    lista_campos = ['Cliente', 'Produto', 'Fornecedor']
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos, state='readonly')
    combo_pesquisa.grid(row=6, column=3, padx=10, pady=5, sticky="w")
    
    
    def salvar_venda(operacao):
        if not valida_campo('Produto', combo_produto.get()):
            form = False
        elif not valida_campo('Cliente', combo_cliente.get()):
            form = False
        elif not valida_campo('Quantidade', txt_quantidade.get()):
            form = False
        elif not valida_campo('moeda', txt_preco_venda.get()):
            form = False
        elif not valida_campo('data', txt_data_venda.get()):
            form = False
        elif not valida_campo('lucro', txt_lucro.get()):
            form = False
        else:
            form = True

        if form:                    
            cliente_id = Cliente.localiza_id_cliente(combo_cliente.get())
            produto_selecionado = combo_produto.get()
            partes = produto_selecionado.split('/')
            nome_produto = partes[0]
            nome_fornecedor = partes[-1]
            produto_id = Produto.localiza_produto_id(nome_produto,nome_fornecedor)        
            quantidade = int(txt_quantidade.get())
            preco_venda= txt_preco_venda.get()        
            data_venda = txt_data_venda.get()
            lucro_original = str(txt_lucro.get()).replace(',','.')                        
            lucro = float(lucro_original)        

            if operacao == 'I':                        
                venda = Venda(data_venda, cliente_id, produto_id, quantidade, preco_venda, lucro)
                venda.salvar_venda()
                limpar_campos()                               
            elif operacao == 'E':
                resposta  = messagebox.askquestion('Cadastro', 'Deseja realmente excluir a venda?', icon='warning')
                if resposta == 'yes':
                    if valida_campo('id', txt_id.get()):
                        id_venda = txt_id.get()
                        venda = Venda(data_venda, cliente_id, produto_id, quantidade, preco_venda, lucro, id_venda)            
                        venda.excluir_venda()
                        limpar_campos()                                    
            else:
                if valida_campo('id', txt_id.get()):
                    id_venda = txt_id.get()
                    venda = Venda(data_venda, cliente_id, produto_id, quantidade, preco_venda, lucro, id_venda)            
                    venda.alterar_venda()
                    limpar_campos()                                    
            
        carregar_vendas()
    
    

    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_venda('I')).grid(row=7, columnspan=2, padx=130, sticky='w')
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_venda('A')).grid(row=7, columnspan=3, pady=10)
    tk.Button(cadastro_janela, text="Excluir", command=lambda:salvar_venda('E')).grid(row=7, columnspan=4, pady=10)

    def ao_selecionar_combo_produto(event):
        produto_selecionado = combo_produto.get()
        partes = produto_selecionado.split('/')
        nome_produto = partes[0]
        nome_fornecedor = partes[-1]        
        valor_sugerido = Venda.calcular_preco_sugerido(nome_produto,nome_fornecedor)        
        lbl_preco_sugerido.config(text=f'Preço sugerido: {valor_sugerido}')

    def ao_sair_preco_venda(event):
        if combo_produto.get() != '' and txt_quantidade.get() != '' and txt_preco_venda.get() != '':            
            preco_venda = txt_preco_venda.get().replace(',','.')
            preco_venda_formatado = float(preco_venda)        
            quantidade = txt_quantidade.get()
            str_preco_sugerido = lbl_preco_sugerido.cget('text')
            partes = str_preco_sugerido.split(':')
            valor_sugerido = partes[-1]
            valor_sugerido_formatado = float(valor_sugerido.replace(',','.'))
            print(valor_sugerido_formatado)        
            if preco_venda_formatado > 0 and valor_sugerido_formatado > 0:
                lucro = (preco_venda_formatado - (valor_sugerido_formatado - 100)) * float(quantidade)
                lucro_formatado = str(round(lucro,2)).replace('.',',')            
                txt_lucro.config(state='normal')
                txt_lucro.delete(0, tk.END)
                txt_lucro.insert(0,lucro_formatado)
                txt_lucro.config(state='disabled')
            else:
                txt_lucro.insert(0,'falhou')        
            


    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get().upper()

        for item in treeview.get_children():
            treeview.delete(item)
        
        
        resultados = Venda.pesquisar_venda(campo,filtro)
        
        for resultado in resultados:
            data_original = resultado[1]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            resultado_lista = list(resultado)
            resultado_lista[1] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(resultado_lista))

        

    combo_produto.bind("<<ComboboxSelected>>", ao_selecionar_combo_produto)
    txt_preco_venda.bind("<FocusOut>", ao_sair_preco_venda)
    combo_produto.bind("<FocusOut>", ao_sair_preco_venda)
    txt_quantidade.bind("<FocusOut>", ao_sair_preco_venda)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)
    
    
    columns = ("ID", "Data", "Cliente", "Produto", "Qtd", "Preço Venda", "Lucro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID", anchor='w')
    treeview.heading("Data", text="Data", anchor='w')
    treeview.heading("Cliente", text="Cliente", anchor='w')
    treeview.heading("Produto", text="Produto", anchor='w')   
    treeview.heading("Qtd", text="Qtd", anchor='w')
    treeview.heading("Preço Venda", text="Preço Venda", anchor='w')
    treeview.heading("Lucro", text="Lucro", anchor='w')    
    treeview.grid(row=8, column=0,columnspan=4, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(cadastro_janela, orient="vertical", command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)

    treeview.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    scrollbar.grid(row=8, column=4, sticky='ns')

    treeview.column("ID",width=30)      
    treeview.column("Data",width=100)
    treeview.column("Preço Venda",width=80)
    treeview.column("Lucro",width=80)
    treeview.column("Qtd",width=30)
    #treeview.column("Cor",width=30)
    #treeview.column("Marca",width=50)
    

    def carregar_vendas():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        # Conectando ao banco de dados e recuperando os dados        
        vendas = Venda.carregar_vendas_treeview()

        # Adicionando os dados na Treeview
        for venda in vendas:
            data_original = venda[1]
    
            # Convertendo o datetime.date para a string formatada dd/mm/yyyy
            data_formatada = data_original.strftime('%d/%m/%Y')
            
            # Converter a tupla cliente em lista para modificar o campo de data
            venda_lista = list(venda)
            venda_lista[1] = data_formatada  # Atualizando o campo de data formatada
            
            # Inserindo os dados na Treeview
            treeview.insert("", "end", values=tuple(venda_lista))               
    
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
            txt_id.config(state='normal')
            txt_id.delete(0,tk.END)
            txt_id.insert(0,item[0])
            txt_id.config(state='disabled')

            txt_data_venda.delete(0,tk.END)
            txt_data_venda.insert(0,item[1])


            combo_cliente.set(item[2])

            combo_produto.set(item[3])

            txt_quantidade.set(item[4])

            txt_preco_venda.delete(0,tk.END)
            txt_preco_venda.insert(0,item[5].replace('.',','))

            txt_lucro.config(state='normal')
            txt_lucro.delete(0,tk.END)
            txt_lucro.insert(0,item[6].replace('.',','))
            txt_lucro.config(state='disabled')
            
            ao_selecionar_combo_produto(event="<<ComboboxSelected>>")
    
    lista_entradas = [txt_id, txt_lucro, txt_preco_venda]
    def limpar_campos():
        for entry in lista_entradas:
            for entry in (lista_entradas):
                if entry == txt_id or entry == txt_lucro: 
                    entry.config(state='normal')
                    entry.delete(0, tk.END)  
                    entry.config(state='disabled')
                else:
                    entry.delete(0, tk.END)

                combo_cliente.set('')
                combo_produto.set('')
                txt_quantidade.set('')
                lbl_preco_sugerido.config(text='Preço Sugerido:')                     

######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)


######################################################################################
# Função para abrir a tela de cadastro de Tipo Produto
def cadastrar_tipo_produto(root):
    # Nova janela para cadastro de cliente
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
    cadastro_janela.title("Cadastro de Tipos de Produto")
    cadastro_janela.geometry("450x450")

    # Campos de entrada    
    tk.Label(cadastro_janela, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Descrição").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(cadastro_janela, text="Margem").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    
    txt_id = tk.Entry(cadastro_janela,state='disabled',disabledbackground='lightgrey',disabledforeground='darkgrey')
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")
    
    txt_descricao = tk.Entry(cadastro_janela)
    txt_descricao.grid(row=1, column=1, padx=9, pady=0, sticky="w")

    txt_margem = tk.Entry(cadastro_janela)
    txt_margem.grid(row=2, column=1, padx=9, pady=0, sticky="w")

    # Função para salvar o cliente
    def salvar_tipo_produto(operacao):
        if not valida_campo('Descrição', txt_descricao.get()):
            form = False
        elif not valida_campo('Margem', txt_margem.get()):
            form = False
        else:
            form = True

        if form:
            tipo_produto = txt_descricao.get().upper()
            margem = float(txt_margem.get())

            if operacao == 'I':
                tipoDeProduto = TipoProduto(tipo_produto,margem)
                tipoDeProduto.salvar_no_banco()
                limpar_campos()
            else:
                if valida_campo('id', txt_id.get()):
                    id = int(txt_id.get())
                    tipoDeProduto = TipoProduto(tipo_produto,margem,id)
                    tipoDeProduto.alterar_no_banco()
                    limpar_campos()
            carregar_tipo_produto()


    # Botão para salvar o cliente
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_tipo_produto('I')).grid(row=3, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_tipo_produto('A')).grid(row=3, columnspan=4, pady=10)

    # Criando a Treeview para exibir os clientes cadastrados
    columns = ("Cod", "Descricao", "Margem")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("Cod", text="Cod", anchor='w')
    treeview.heading("Descricao", text="Descricao", anchor='w')
    treeview.heading("Margem", text="Margem", anchor='w')    
    treeview.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    treeview.column("Cod",width=30)

    def carregar_tipo_produto():
        # Limpa a Treeview antes de carregar os dados
        for item in treeview.get_children():
            treeview.delete(item)

        tipos_produtos = TipoProduto.carregar_tipos_produto_treeview()

        # Adicionando os dados na Treeview
        for tipo in tipos_produtos:
            treeview.insert("", "end", values=tipo)
        
    def ao_clicar_treeview(event):
        item_selecionado = treeview.selection()
        #id, nome, telefone, data_cad
        if item_selecionado:
            item = treeview.item(item_selecionado, 'values')
            print(item)
            txt_id.config(state='normal')
            txt_id.delete(0,tk.END)                        
            txt_id.insert(0,item[0])
            txt_id.config(state='disabled')

            txt_descricao.delete(0,tk.END)
            txt_descricao.insert(0,item[1])

            txt_margem.delete(0,tk.END)
            txt_margem.insert(0,item[2])

    lista_entradas = [txt_id, txt_descricao, txt_margem]                  
    def limpar_campos():
        for entry in lista_entradas:
            if entry == txt_id: 
                entry.config(state='normal')
                entry.delete(0, tk.END)  
                entry.config(state='disabled')
            else:
                entry.delete(0, tk.END)
            txt_descricao.focus()
    # Carregar clientes ao abrir a janela
    carregar_tipo_produto()
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview)
######################################################################################
