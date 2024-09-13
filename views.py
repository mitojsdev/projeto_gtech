import tkinter as tk
from tkinter import ttk
from datetime import datetime
from modelos import Cliente, Fornecedor, TipoProduto, Produto
from funcoes import valida_campo


def cadastrar_cliente(root):
    # Nova janela para cadastro de cliente
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
    #odal_window.grab_set()
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
    combo_pesquisa = ttk.Combobox(cadastro_janela,values=lista_campos)
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
            nome = txt_nome.get()
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



    ##############################################################################

    ######################################################################################
#função para cadastrar fornecedor
def cadastrar_fornecedor(root):
    
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.grab_set()
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

    txt_id = tk.Entry(cadastro_janela,state='disabled', disabledbackground='lightgrey',disabledforeground='darkgrey')
    txt_id.grid(row=0, column=1, padx=9, pady=0, sticky="w")

    txt_nome_empresa = tk.Entry(cadastro_janela,width=50)
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
            nome = txt_nome_empresa.get()
            tipo_empresa = combo_tipo_empresa.get()
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
        
        fornecedores = Fornecedor.carregar_fornecedores_treeview()

        # Adicionando os dados na Treeview
        for fornecedor in fornecedores:
            treeview.insert("", "end", values=fornecedor)
                
    
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
        filtro = txt_pesquisa.get()
        
        for item in treeview.get_children():
            treeview.delete(item)
        
        resultados = Fornecedor.pesquisa_fornecedor(campo, filtro)
        
        for resultado in resultados:
            treeview.insert("", "end", values=resultado)
        
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
    combo_fornecedor = ttk.Combobox(cadastro_janela, values=lista_fornecedores, width=50)
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
        else:
            form = True

        if form:        
            nome = txt_nome.get()                        
            preco_custo = float(txt_preco_custo.get().replace(',','.'))            
            tipo_produto = combo_tipo_produto.get()                
            tipo_produto_id = TipoProduto.localiza_tipo_produto(tipo_produto)            
            fabricante = txt_fabricante.get()            
            marca = txt_marca.get()            
            cor = txt_cor.get()            
            fornecedor = Fornecedor.localiza_id_fornecedor(combo_fornecedor.get())            
            data_cadastro = txt_data_cadastro.get()
        
            if operacao == 'I':
                produto = Produto(nome, preco_custo, tipo_produto_id, fabricante, marca, cor, fornecedor, data_cadastro)
                produto.salvar_produto()
                limpar_campos()
            else:
                if valida_campo('id', txt_id.get()):
                    id_produto = txt_id.get()
                    produto = Produto(nome, preco_custo, tipo_produto_id, fabricante, marca, cor, fornecedor, data_cadastro, id_produto)
                    produto.alterar_produto()
                    limpar_campos()
        carregar_produtos()        
               
    tk.Button(cadastro_janela, text="Incluir", command=lambda:salvar_produto('I')).grid(row=9, columnspan=2, pady=10)
    tk.Button(cadastro_janela, text="Alterar", command=lambda:salvar_produto('A')).grid(row=9, columnspan=3, pady=10)
    
    
    columns = ("ID", "Nome Produto", "Preço Custo", "Tipo", "Fabricante", "Marca", "Cor", "Fornecedor", "Data de Cadastro")
    treeview = ttk.Treeview(cadastro_janela, columns=columns, show="headings")
    treeview.heading("ID", text="ID", anchor='w')
    treeview.heading("Nome Produto", text="Nome Produto", anchor='w')
    treeview.heading("Preço Custo", text="Preço Custo", anchor='w')
    treeview.heading("Tipo", text="Tipo", anchor='w')
    treeview.heading("Fabricante", text="Fabricante", anchor='w')
    treeview.heading("Marca", text="Marca", anchor='w')
    treeview.heading("Cor", text="Cor", anchor='w')
    treeview.heading("Fornecedor", text="Fornecedor", anchor='w')
    treeview.heading("Data de Cadastro", text="Data de Cadastro", anchor='w')
    treeview.grid(row=10, column=0,columnspan=3, padx=10, pady=10)

    treeview.column("ID",width=30)
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
            treeview.insert("", "end", values=produto)
        
        
    
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

            txt_data_cadastro.delete(0,tk.END)
            txt_data_cadastro.insert(0,item[8])
            
            #ao_selecionar_combo_produto(event="<<ComboboxSelected>>")
    def ao_digitar_pesquisa(event):
        campo = combo_pesquisa.get()
        filtro = txt_pesquisa.get()
        
        for item in treeview.get_children():
            treeview.delete(item)
            resultados = Produto.pesquisar_produtos(campo,filtro)
        
        for resultado in resultados:
            treeview.insert("", "end", values=resultado)
    
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

        txt_nome.focus()
        
######################################################################################    
    treeview.bind("<ButtonRelease-1>", ao_clicar_treeview_produto)
    txt_pesquisa.bind("<KeyRelease>", ao_digitar_pesquisa)

# fim tela cadastro produtos
######################################################################################
