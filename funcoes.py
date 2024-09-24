from tkinter import messagebox
from datetime import datetime
import re
import openpyxl
from openpyxl import Workbook
from tkinter import filedialog



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
                        
    elif tipo_campo == 'Nome_Produto':
            if '/' in valor:
                messagebox.showwarning('Atenção!', 'O nome do produto não deve conter "/" ou outros caracteres especiais.')
                return False
            else:
                return True
    else:
        if valor == '':
            messagebox.showwarning('Campos obrigatórios', f'O seguinte campo não pode ser vazio: {tipo_campo}.')
            resultado = False
        else:
            resultado = True
       
    return resultado


def exportar_excel(tabela, titulo):
    wb = Workbook()
    ws = wb.active
    ws.title = titulo

    colunas = [tabela.heading(col)['text'] for col in tabela["columns"]]
    ws.append(colunas)

    # Adicionar as linhas da Treeview
    for item in tabela.get_children():        
        valores = tabela.item(item)["values"]

        # Converter valores numéricos com ponto para vírgula
        valores_convertidos = []
        for valor in valores:
            try:
                # Tentar converter para float
                valor_convertido = float(valor)
            except (ValueError, TypeError):
                # Se não for possível converter, manter o valor original
                valor_convertido = valor
            valores_convertidos.append(valor_convertido)
        
        ws.append(valores_convertidos)
        #ws.append(valores)

    # Abrir uma janela de diálogo para salvar o arquivo
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    
    if caminho_arquivo:
        wb.save(caminho_arquivo)        
        messagebox.showinfo('Cadastro', f'O arquivo foi salvo em {caminho_arquivo}')
