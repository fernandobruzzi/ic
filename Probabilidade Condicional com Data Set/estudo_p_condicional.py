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
    
    df["Country"].value_counts().plot(ax = axes[0][0], kind = 'barh', fontsize= 9, log=True)    
    axes[0][0].title.set_text("Concentração de endossimbiontes no mundo")

    df["Clade"].value_counts().plot(ax = axes[0][1], kind = "barh", log= True)
    axes[0][1].title.set_text("Concentração de endossimbiontes por clade(evoluíram de um mesmo ancestral)")

    #pegamos os dois países com mais registros de endossimbiontes
    df_australia = df[df["Country"]=="Australia"]
    df_p_maior_diversidade = df[df["Country"]==p_diverso]
    
    #adicionamos no grafico a distribuicao dos clade
    # df_australia["Clade"].value_counts().plot(ax = axes[1][0], kind = 'pie', y ='', autopct = '%1.0f%%')
    df_australia["Clade"].value_counts().plot(ax = axes[1][0], kind = 'barh', log = True)
    axes[1][0].title.set_text("Quantidade de especies por clades na Austrália")

    # df_p_maior_diversidade["Clade"].value_counts().plot(ax = axes[1][1], kind = 'pie', y ='', autopct = '%1.0f%%')
    df_p_maior_diversidade["Clade"].value_counts().plot(ax = axes[1][1], kind = 'barh', log = True)
    axes[1][1].title.set_text(f"Quantidade de especies por clades de clades no(a) {p_diverso}")

    plt.show()
    plt.clf()
    return

def pais_com_maior_diversidade(df):
    paises = df["Country"].unique()
    tipos_clade = np.zeros((len(paises),))
    for p in range(len(paises)):
        tipos_clade[p] = (df[df["Country"] == paises[p]])["Clade"].nunique()
    return paises[np.argmax(tipos_clade)] 

def probabilidades_condicionais(df):
    #selecionamos os eventos a serem considerados
    field = ["Clade", "Gene", "Host_Phylum","Host_Class", "Environment", "Ocean", "Country", "T_MMM_05"]
    #criamos o arquivo de excell
    workbook = xlsxwriter.Workbook('ic/Probabilidade Condicional com Data Set/p_condicionais.xlsx')
    worksheet = workbook.add_worksheet()
    i = 0
    j = 0
    row = 0
    column = 0
    #removemos os valores vazios
    df.dropna()
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
                worksheet.write(row, column, f"P(A)")
                column+=1
                worksheet.write(row, column, f"Indepente")
                column -=4        
                row += 1
                for a in A:
                    for b in B:
                        p_a = (len(df.query(f'{i} == "{a}"')))/total_elementos
                        p_b = (len(df.query(f'{j} == "{b}"')))/total_elementos
                        p_a_inter_b = (len(df.query(f'{i} == "{a}" and {j} == "{b}"')))/total_elementos
                        
                        if p_b == 0:
                            p_a_considerando_b = 0
                        else:
                            p_a_considerando_b = (p_a_inter_b)/(p_b)
                        
                        # vamos fazer um teste de compatibilidade entre p(a) e p(a|b) para termos certeza de independencia quando eles forem bem parecidos
                        epsilon = 5.96e-08
                        if p_a != 0: 
                            if(np.abs((p_a_considerando_b/p_a)-1)) < epsilon:
                                s = 'Sim'
                            else: s = 'Não'
                        else:
                            s='Sim'

                        p_a_considerando_b = round(p_a_considerando_b, 3)
                        p_a = round(p_a,3)


                        worksheet.write(row, column, f"{a}")
                        column+=1
                        worksheet.write(row, column, f"{b}")
                        column+=1
                        worksheet.write(row, column, f"{p_a_considerando_b}")
                        column+=1
                        worksheet.write(row, column, f"{p_a}")
                        column+=1
                        worksheet.write(row, column, f"{s}")
                        column -=4
                        row+=1
                column+=6
                row = 0      
    workbook.close()
    return 0

def dist_a_em_b(a, b, df):
    # df_australia["Clade"].value_counts().plot(ax = axes[1][0], kind = 'pie', y ='', autopct = '%1.0f%%')
    # axes[1][0].title.set_text("Distribuição de clades na Austrália")
    df = df[df[f"{b[0]}"]==f"{b[1]}"]
    df[f"{a[0]}"].value_counts().plot(kind = 'pie', autopct = '%1.0f%%')
    plt.show()
    plt.clf()
    return

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
path_geos = 'ic/Probabilidade Condicional com Data Set/GeoSymbio e infos.xlsx'
df_geos = pd.read_excel(io = path_geos)

# pegamos informações basicas do df
df_geos.info()
df_geos.describe()

pais_diverso = pais_com_maior_diversidade(df_geos)
dist_endo_pais(df_geos, pais_diverso)

# geramos um aqruibo com as probabilidades condicionais entre os eventos  ["Clade", "Gene", "Host_Phylum","Host_Class", "Environment", "Ocean", "Country", "T_MMM_05"]
# probabilidades_condicionais(df_geos)

path_pcond = 'ic/Probabilidade Condicional com Data Set/p_condicionais.xlsx'
df_pcond = pd.read_excel(io = path_pcond)

df_pcond.info()
df_pcond.describe()
print(df_pcond)

a = ['Clade']
b = ['Country', 'Philippines']
# dist_a_em_b(a,b,df_geos)



