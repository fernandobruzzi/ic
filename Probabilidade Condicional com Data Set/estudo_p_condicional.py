import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter

# print(df)
# print(df.loc[df["Country"]=="Japan"])
# talvez seja uma boa primeiro fazer uma filtragem e ver se temos eventos independentes? calcula o p(a/b) deles só se p(a,b) = p(a)p(b      )
# print(df.head())
# a = df["Country"].value_counts().head()
# print(a)

def dist_endo_pais(df, p_diverso):
    #checamos a distribuicao de endossimbioentes por país e outras informações
    fig, axes = plt.subplots(nrows=2 , ncols= 2)
    
    df["Country"].value_counts().plot(ax = axes[0][0], kind = 'barh', fontsize= 9)    
    axes[0][0].title.set_text("Distribuição de endossimbiontes no mundo")

    df["Clade"].value_counts().plot(ax = axes[0][1], kind = "barh")
    axes[0][1].title.set_text("Distribuição de encodssimbiontes por clade(evoluíram de um mesmo ancestral)")

    #pegamos os dois países com mais registros de endossimbiontes
    df_australia = df[df["Country"]=="Australia"]
    df_p_maior_diversidade = df[df["Country"]==p_diverso]
    
    #adicionamos no grafico a distribuicao dos clade
    df_australia["Clade"].value_counts().plot(ax = axes[1][0], kind = 'pie', y ='', autopct = '%1.0f%%')
    axes[1][0].title.set_text("Distribuição de clades na Austrália")

    df_p_maior_diversidade["Clade"].value_counts().plot(ax = axes[1][1], kind = 'pie', y ='', autopct = '%1.0f%%')
    axes[1][1].title.set_text(f"Distribuição de clades no(a) {p_diverso}")

    plt.show()
    return

def pais_com_maior_diversidade(df):
    paises = df["Country"].unique()
    tipos_clade = np.zeros((len(paises),))
    for p in range(len(paises)):
        tipos_clade[p] = (df[df["Country"] == paises[p]])["Clade"].nunique()
    return paises[np.argmax(tipos_clade)] 

def probabilidades_condicionais(df):
    #selecionamos os eventos a serem considerados
    field = ["Clade", "Gene", "Host_Phylum","Host_Class", "Environment", "Ocean", "Country"]
    #criamos o arquivo de excell
    workbook = xlsxwriter.Workbook('ic/Probabilidade Condicional com Data Set/p_condicionais.xlsx')
    worksheet = workbook.add_worksheet()
    i = 0
    j = 0
    row = 0
    column = 0
    total_elementos = len(df)
    for i in field:
        A = df[i].unique()
        for j in field:
            if i != j: 
                B = df[j].unique()
                worksheet.write(row , column, f"A = {i}")
                column+=1
                worksheet.write(row, column, f"B = {j}",)
                column+=1
                worksheet.write(row, column, f"P(A|B)")
                column+=1
                worksheet.write(row, column, f"P(A)P(B)")
                column -=3        
                row += 1
                for a in A:
                    for b in B:
                        p_a = (len(df.query(f'{i} == "{a}"')))/total_elementos
                        p_b = (len(df.query(f'{j} == "{b}"')))/total_elementos
                        p_a_inter_b = (len(df.query(f'{i} == "{a}" and {j} == "{b}"')))/total_elementos
                        p_a_considerando_b = round((p_a_inter_b)/(p_b), 3)
                        p_a_vezes_p_b = round(p_a*p_b, 3)
                        worksheet.write(row, column, f"{a}")
                        column+=1
                        worksheet.write(row, column, f"{b}")
                        column+=1
                        worksheet.write(row, column, f"{p_a_considerando_b}")
                        column+=1
                        worksheet.write(row, column, f"{p_a_vezes_p_b}")
                        column -=3
                        row+=1
                column+=5
                row = 0      
    workbook.close()
    return 0

# def rand_vars(df):
#     df = df [['Clade','Gene','Host_Family','Ocean','Country']]    
#     #vamos determinar um conjunto de Indicadores I['x'] x = clade, gene...
#     I = {
#         'Clade':[],
#         'Gene':[],
#         'Host_Family':[],
#         'Ocean': [],
#         'Country': []
#     }
#     #Para o indicador por exemplo I(Clade(A)), temos que o indice i da lista com os clades é o valor da variavel aleatória I(clade) = i
#     for j in I:
#         valores = df[j].unique()
#     return 1


# lemos o dataframe
path = 'ic/Probabilidade Condicional com Data Set/GeoSymbio e infos.xlsx'
df = pd.read_excel(io = path)

# pegamos informações basicas do df
df.info()
df.describe()

# pais_diverso = pais_com_maior_diversidade(df)
# # print(pais_diverso, type(pais_diverso))
# dist_endo_pais(df, pais_diverso)

# probabilidades_condicionais(df)


