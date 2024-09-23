from conexao import conectar
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def buscar_lucro_por_mes():

    conexao = conectar()
    cursor= conexao.cursor()

   

    #cursor que busca venda por mês
    # cursor.execute('''
    #         SELECT EXTRACT(DAY FROM "DATA")::int, COUNT(*) 
    #         FROM "TB_VENDA"
    #         WHERE EXTRACT(MONTH FROM "DATA") = %s AND EXTRACT(YEAR FROM "DATA") = %s
    #         GROUP BY EXTRACT(DAY FROM "DATA")
    #         ORDER BY EXTRACT(DAY FROM "DATA")
    #     ''', (mes_atual, ano_atual))
    
    #consulta de lucro por mês
    cursor.execute('''
    SELECT 
        EXTRACT(YEAR FROM "DATA") AS ano,
        EXTRACT(MONTH FROM "DATA") AS mes,
        SUM("LUCRO") AS lucro_mensal
    FROM 
    "TB_VENDA"
    GROUP BY 
        EXTRACT(YEAR FROM "DATA"), EXTRACT(MONTH FROM "DATA")
    ORDER BY 
        ano, mes;''')


    lucro = cursor.fetchall()
    conexao.close
    return lucro

def criar_grafico(root):
    vendas = buscar_lucro_por_mes()
    meses = [f'{venda[0]}/{venda[1]}' for venda in vendas]  # Combinação de ano/mês
    lucros = [venda[2] for venda in vendas]

    fig, ax = plt.subplots()
    ax.bar(meses, lucros, color='green')

    ax.set_title('Lucro por Mês')
    ax.set_xlabel('Mês/Ano')
    ax.set_ylabel('Lucro Total')

    # Ajustar os ticks para os meses
    ax.set_xticks(range(len(meses)))
    ax.set_xticklabels(meses, rotation=45)  # Rotacionar os labels para melhor visualização

    # Exibir o gráfico no tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

