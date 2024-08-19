import numpy as np
import matplotlib.pyplot as plt

class Dado_Ideal:
    
    def __init__(self, faces):
        #determina os atributos faces e o historico de cada face 
        self.faces = faces
        self.historico_das_faces = np.zeros((1,faces+1))
        self.vezes_jogadas = np.zeros((1), dtype = int)
        self.link_freq_jog = 0 #esse link serve para relacionar historico[link][x] com jogadas[link]

        #sorteamos uma face para monitorar
        # self.face_monitorada = np.random.randint(1, faces + 1) 
        # para efeitos do experimento vou setar a face monitorada como a 6 
        self.face_monitorada = 6  
        self.contador_face_monitorada = 0
        self.vetor_face_monitorada = []


        
        
    def jogar_dado(self, vezes):

        #atualiza quantas vezes o dado já foi jogado no total
        self.vezes_jogadas = np.append(self.vezes_jogadas, [self.vezes_jogadas[self.link_freq_jog] + vezes])

        #gera os resultados
        resultado = np.random.randint(1, self.faces + 1, vezes)
        
        #cria a lista para armazenar os resultados dessa jogada com cada posicao correspondendo a uma face
        resultados_nessa_jogada = np.zeros((self.faces+1,), dtype=int)

        #percorre os resultados e adiciona no historico e nos resultados dessa jogada e na quantiadade de jogadas ate sair x face
        for i in np.nditer(resultado):
            resultados_nessa_jogada[i]+= 1
            #atualizamos o contador da nossa face monitorada, estamos considerando X = numero de jogadas para sair face monitorada X ~ FirstSucess(5/6), FirstSucess(p) = 1 + Y ~  Geometry(p)
            self.contador_face_monitorada+= 1
            
            if i == self.face_monitorada:
                self.vetor_face_monitorada+= [self.contador_face_monitorada]
                self.contador_face_monitorada = 0


        self.historico_das_faces = np.append(self.historico_das_faces,[self.historico_das_faces[self.link_freq_jog] + resultados_nessa_jogada],axis=0)  

        self.link_freq_jog+=1
        #quando retornamos o resultado para a funcao print retornamos só a partir do resultado da face 1, já que a face 0 é sempre 0
        return (f"Os resultados obtidos foram: {resultados_nessa_jogada[1:]}\n"
    f"E a diferenca entre a face que apareceu mais vezes e a que apareceu menos vezes é {resultados_nessa_jogada.max() - resultados_nessa_jogada.min()}\n"
    f"E o historico dos resultados é {self.historico_das_faces[1:][:]}\n")         
    
    
    def grafico_jogadas(self):
        #gera os dados para construcao do histograma e constroi o histograma
        data = []
        for face, frequencia in enumerate(self.historico_das_faces[self.link_freq_jog]):
            data+= [face] * int(frequencia)
        plt.hist(data, bins = range(1,self.faces+2), density = True, align= 'left', color = 'skyblue', edgecolor = 'black')
        plt.xticks(range(1, self.faces+1))
        plt.xlabel("Face")
        plt.ylabel("Frequência relativa")
        plt.title(f"Frequência relativa de cada face para dado jogado {self.vezes_jogadas[self.link_freq_jog]} vezes")
        # plt.show()

    
    def grafico_erro(self):
        y = self.historico_das_faces[1:, 1:] 
        x = self.vezes_jogadas[1:]
        
        #extraimos as frequencias
        for i in range(len(x)):
            y[i] = y[i]/x[i]

        #transformamos as frequencias em frequencias - frequencia ideal
        freq_ideal = (1/self.faces)
        y = np.absolute((y - freq_ideal))
        
        for i in range(self.faces):
            plt.plot(x, y[:, i], label = f"face{i+1}", linestyle = "dotted", alpha = 0.8)
    

        #alem disso, vamos inserir retas para ver qual se adequa ao erro
        plt.plot(x,1/x, label = "1/x", alpha = 0.6)
        # plt.plot(x,1/(x**2), label = "1/x**2")
        # plt.plot(x,1/np.log(x), label = "1/ln(x)")
        # plt.plot(x, 1/x*(np.log(x)), label = "1/x*ln(x)")

        plt.xlabel("Vezes jogadas")
        plt.ylabel("Módulo(Frequencia real da face - frequencia ideal)")
        plt.yscale("log")
        plt.xscale("log")
        plt.title(f"Vezes jogadas{self.vezes_jogadas[-1]}")
        plt.legend()
        # plt.show()


    def grafico_face_monitorada(self):
        #se a face nao tiver saido nao fazemos nada ou ela tiver saído nas primeiras vezes que eu jogar
        if not self.vetor_face_monitorada or (len(np.unique(self.vetor_face_monitorada))== 1 and (0 in np.unique(self.vetor_face_monitorada))): return
        data = self.vetor_face_monitorada
        media = np.mean(data)
        mediana = np.median(data)
        desvio_padrao = np.std(data)

        valor_esperado = (((self.faces-1)/self.faces)/(1/self.faces)) + 1 
        plt.hist(data, bins = range(np.min(data)-1, np.max(data)+2), align= 'left', density = True, color = 'skyblue', edgecolor = 'black'  )
        plt.xticks(range(np.min(data)-1, np.max(data)+2))
        plt.xlabel("Quantidade de lançamentos")
        plt.ylabel("Porcentagem dos lançamentos")
        plt.text(x = (np.max(data)/(2)), y = ((1/self.faces)/2), s = f"média = {media:.4f} \n valor esperado = {valor_esperado:.4f} \n mediana = {mediana} \n desvio padrão = {desvio_padrao:.4f}")
        plt.title(f"Histograma que mostra quantas vezes foram jogadas o dado até que a face {self.face_monitorada} fosse obtida")
        plt.tight_layout()
        # plt.show()

# d = Dado_Ideal(6)
# for i in range (20):
#     d.jogar_dado(2**i)
#     if i != 0 and 20%i == 0:
#         d.grafico_face_monitorada()
#         plt.show()