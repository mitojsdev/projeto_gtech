from conexao import conectar
from tkinter import messagebox
from datetime import datetime


def valida_campo(tipo_campo, valor):
    if tipo_campo == 'id':
        try:
            numero = int(valor)
            resultado = True
        except ValueError:
            messagebox.showwarning('Erro de valor', 'Selecione um registro na tabela para alterar.')
            resultado = False
    elif tipo_campo == 'data':
        try:
            datetime.strptime(valor, '%d/%m/%Y')
            resultado = True
        except ValueError:
            messagebox.showwarning('Data inválida', 'Informe a data no formato dd/mm/aaaa.')
            resultado = False
    elif tipo_campo == 'nome' or tipo_campo == 'telefone':
        if valor == '':
            messagebox.showwarning('Campos obrigatórios', f'O seguinte campo não pode ser vazio: {tipo_campo}.')
            resultado = False
        else:
            resultado = True
       
    return resultado