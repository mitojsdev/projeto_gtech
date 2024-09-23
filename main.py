import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from views import cadastrar_cliente, cadastrar_produto, cadastrar_tipo_produto
from views import cadastrar_fornecedor, cadastrar_venda, pesquisar_vendas
import os
from graficos import criar_grafico

def fechar_janela():
    global root
    root.quit()
    root.destroy()

# Criação da janela principal
def criar_interface():
    global root
    root = tk.Tk() 
    root.title("GTECH Control 1.0")
    root.geometry("1200x600")

     # Configurar o evento de fechar a janela
    root.protocol("WM_DELETE_WINDOW", fechar_janela)

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
    menu_produto.add_command(label="Tipo de Produto", command=lambda:cadastrar_tipo_produto(root))
    menu_produto.add_separator()
    menu_barra.add_cascade(label="Produto",menu=menu_produto)

    menu_venda = tk.Menu(menu_barra,tearoff=0)
    menu_venda.add_command(label="Cadastro", command=lambda:cadastrar_venda(root))
    menu_venda.add_separator()
    menu_venda.add_command(label="Pesquisa", command=lambda:pesquisar_vendas(root))
    menu_barra.add_cascade(label="Venda", menu=menu_venda)

    root.config(menu=menu_barra)

    # Obter o caminho absoluto do diretório do programa
    diretorio_programa = os.path.dirname(os.path.abspath(__file__))

    # Construir o caminho completo para a imagem dentro da pasta "midia"
    caminho_imagem = os.path.join(diretorio_programa, "midia", "gtech_logo.png")
    #caminho_imagem = 'gtech_logo.png'

    # Carregar a imagem da logo
    logo = PhotoImage(file=caminho_imagem)

    # Inserir a imagem no centro da tela
    label_logo = tk.Label(root, image=logo)
    label_logo.image = logo  # Manter referência para evitar garbage collection
    label_logo.pack(pady=20)

    versao = '1.0.2'
    # Criar um label no rodapé da tela
    label_rodape = tk.Label(root, text=f"versão {versao}", font=("Montserrat", 10))
    label_rodape.pack(side="bottom", pady=10)  # Posiciona o label no rodapé da tela


    criar_grafico(root)


    # Inicia o loop principal da interface
    root.mainloop()

criar_interface()
