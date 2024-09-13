from tkinter import messagebox
from datetime import datetime
import re


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
    elif tipo_campo == 'moeda':        
        # Expressão regular para validar um número com até duas casas decimais
        padrao = r'^\d+,\d{1,2}$|^\d+$'
        
        valor_moeda = re.match(padrao,valor)
        if valor_moeda != None:                       
            resultado = True
        else:
            messagebox.showwarning('Atenção!', 'O valor do Preço de custo é inválido.')
            resultado = False
                        
    #elif tipo_campo == 'nome' or tipo_campo == 'telefone' or tipo_campo == 'tipo_empresa' or tipo_campo == 'tipo_produto' or tipo_campo == 'fabricante' or tipo_campo == 'cor' or tipo_campo == 'marca' or tipo_campo == 'fornecedor':
    else:
        if valor == '':
            messagebox.showwarning('Campos obrigatórios', f'O seguinte campo não pode ser vazio: {tipo_campo}.')
            resultado = False
        else:
            resultado = True
       
    return resultado