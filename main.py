#import funcoes as fct
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modelos import TipoProduto
from conexao import conectar
from tkinter import PhotoImage
from views import cadastrar_cliente, cadastrar_produto
from views import cadastrar_fornecedor, cadastrar_venda
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
menu_fornecedor.add_command(label="Cadastro",command=lambda:cadastrar_fornecedor(root))
menu_barra.add_cascade(label="Fornecedor",menu=menu_fornecedor)


menu_produto = tk.Menu(menu_barra,tearoff=0)
menu_produto.add_command(label="Cadastro", command=lambda:cadastrar_produto(root))
menu_produto.add_command(label="Tipo de Produto", command=cadastrar_tipo_produto)
menu_produto.add_separator()
menu_barra.add_cascade(label="Produto",menu=menu_produto)

menu_venda = tk.Menu(menu_barra,tearoff=0)
menu_venda.add_command(label="Cadastro", command=lambda:cadastrar_venda(root))
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
