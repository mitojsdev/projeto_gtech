import tkinter as tk
from tkinter import ttk

# Função chamada quando o botão "Cadastrar" é clicado
def submit_form():
    # Apenas para exibir uma mensagem de aviso, sem interação com banco de dados
    tk.messagebox.showinfo("Cadastro", "Ação de cadastrar simulada.")

# Configuração da janela principal
root = tk.Tk()
root.title("GTECH IMPORTS - CADASTRO")

# Criação do formulário
frame_form = tk.Frame(root, padx=10, pady=10)
frame_form.pack(padx=20, pady=20)

# Campo Nome
tk.Label(frame_form, text="Nome do Cliente").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_nome = tk.Entry(frame_form, width=30)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

# Campo Produto
tk.Label(frame_form, text="Produto").grid(row=1, column=0, padx=5, pady=5, sticky='e')
combo_produto = ttk.Combobox(frame_form, values=["Produto A", "Produto B", "Produto C"], width=27)
combo_produto.grid(row=1, column=1, padx=5, pady=5)

# Campo Data
tk.Label(frame_form, text="Data (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_data = tk.Entry(frame_form, width=30)
entry_data.grid(row=2, column=1, padx=5, pady=5)

# Campo Tipo de Ação
tk.Label(frame_form, text="Tipo de Ação").grid(row=3, column=0, padx=5, pady=5, sticky='e')
combo_acao = ttk.Combobox(frame_form, values=["Venda", "Estoque"], width=27)
combo_acao.grid(row=3, column=1, padx=5, pady=5)

# Botão Cadastrar
btn_submit = tk.Button(frame_form, text="Cadastrar", command=submit_form)
btn_submit.grid(row=4, column=0, columnspan=2, pady=10)

# Frame para Treeview (Apenas visualização)
frame_tree = tk.Frame(root)
frame_tree.pack(padx=20, pady=20)

# Configuração da Treeview
columns = ("id", "nome", "produto", "data", "acao")
tree = ttk.Treeview(frame_tree, columns=columns, show='headings')
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("produto", text="Produto")
tree.heading("data", text="Data")
tree.heading("acao", text="Ação")
tree.pack(fill=tk.BOTH, expand=True)

# Iniciar a interface
root.mainloop()
