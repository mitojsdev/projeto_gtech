from conexao import conectar
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def buscar_vendas_mes_atual():

    conexao = conectar()
    cursor= conexao.cursor()

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    cursor.execute('''
            SELECT EXTRACT(DAY FROM "DATA")::int, COUNT(*) 
            FROM "TB_VENDA"
            WHERE EXTRACT(MONTH FROM "DATA") = %s AND EXTRACT(YEAR FROM "DATA") = %s
            GROUP BY EXTRACT(DAY FROM "DATA")
            ORDER BY EXTRACT(DAY FROM "DATA")
        ''', (mes_atual, ano_atual))

    vendas_dia = cursor.fetchall()
    conexao.close
    return vendas_dia

def criar_grafico(root):
    vendas = buscar_vendas_mes_atual()
    dias = [venda[0] for venda in vendas]
    qtd_vendas = [venda[1] for venda in vendas]

    fig, ax = plt.subplots()
    ax.bar(dias, qtd_vendas, color='blue')
    
    ax.set_title(f'Vendas no Mês {datetime.now().strftime("%B")}')
    ax.set_xlabel('Dia')
    ax.set_ylabel('Quantidade de Vendas')

    ax.set_xticks(dias)
    ax.set_yticks(qtd_vendas)
    
    # Exibir o gráfico no tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

