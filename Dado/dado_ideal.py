import numpy as np
import matplotlib.pyplot as plt

class Dado_Ideal:
    
    def __init__(self, faces):
        #determina os atributos faces e o historico de cada face 
        self.faces = faces
        self.historico_das_faces = np.zeros((1,faces+1))
        self.vezes_jogadas = np.zeros((1), dtype = int)
        self.link_freq_jog = 0 #esse link serve para relacionar historico[link][x] com jogadas[link]
        self.jogadas_media_ate_sair = np.zeros(faces+1)        

        
        
    def jogar_dado(self, vezes):

        #atualiza quantas vezes o dado já foi jogado no total
        self.vezes_jogadas = np.append(self.vezes_jogadas, [self.vezes_jogadas[self.link_freq_jog] + vezes])

        #gera os resultados
        resultado = np.random.randint(1, self.faces + 1, vezes)
        
        #cria a lista para armazenar os resultados dessa jogada com cada posicao correspondendo a uma face
        resultados_nessa_jogada = np.zeros((self.faces+1,), dtype=int)

        #percorre os resultados e adiciona no historico e nos resultados dessa jogada e na quantiadade de jogadas ate sair x face
        contador = 0
        anterior = resultado[0]
        for i in np.nditer(resultado):
            resultados_nessa_jogada[i]+= 1

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
        plt.show()

    
    def grafico_erro(self):
        y = self.historico_das_faces[1:, 1:]
        x = self.vezes_jogadas[1:]

        #extraimos as frequencias
        for i in range(len(x)):
            y[i] = y[i]/x[i]

        #transformamos as frequencias em frequencias - frequencia ideal
        freq_ideal = (1/self.faces)
        y = y - freq_ideal
        for i in range(self.faces):
            plt.plot(x, y[:, i], label = f"face{i+1}")

        #alem disso, vamos inserir retas para ver qual se adequa ao erro
        plt.plot(x,1/x, label = "1/x")
        plt.plot(x,1/(x**2), label = "1/x**2")
        plt.plot(x,1/np.log(x), label = "1/ln(x)")
        plt.plot(x, 1/x*(np.log(x)), label = "1/x*ln(x)")

        plt.xlabel("Vezes jogadas")
        plt.ylabel("Frequencia real da face - frequencia ideal")
        plt.legend()
        plt.show()




dado1 = Dado_Ideal(4)

for i in range (10):
    # print(dado1.jogar_dado(2**i))
    dado1.jogar_dado(2**i)
dado1.grafico_erro()




