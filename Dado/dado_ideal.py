import numpy as np
import matplotlib.pyplot as plt

class Dado_Ideal:
    
    def __init__(self, faces):
        #determina os atributos faces e a frequencia de cada face 
        self.faces = faces
        self.frequencia_das_faces = np.zeros((faces+1,), dtype=int)
        self.vezes_jogadas = 0
        self.testevezes = np.zeros((),dtype=int)
        
        #somamos +1 no vetor que guarda a frequência para fazer com que a face 1 fique na posicao 1 do vetor
        
        
    def jogar_dado(self, vezes):
        #atualiza quantas vezes o dado ja foi jogado:
        self.vezes_jogadas += vezes

        #gera os resultados
        resultado = np.random.randint(1, self.faces + 1, vezes)
        
        #cria a lista para armazenar os resultados dessa jogada com cada posicao correspondendo a uma face
        resultados_nessa_jogada = np.zeros((self.faces+1,), dtype=int)

        #percorre os resultados e adiciona no historico e nos resultados dessa jogada
        for i in np.nditer(resultado):
            resultados_nessa_jogada[i]+= 1
            self.frequencia_das_faces[i]+=1

        #quando retornamos o resultado para a funcao print retornamos só a partir do resultado da face 1, já que a face 0 é sempre 0
        return (f"Os resultados obtidos foram: {resultados_nessa_jogada[1:]}\n"
    f"E a diferenca entre a face que apareceu mais vezes e a que apareceu menos vezes é {resultados_nessa_jogada.max() - resultados_nessa_jogada.min()}\n"
    f"E o historico dos resultados é {self.frequencia_das_faces[1:]}\n")         
    
    
    def grafico_jogadas(self):
        #gera os dados para construcao do histograma e constroi o histograma
        data = []
        for face, frequencia in enumerate(self.frequencia_das_faces):
            data+= [face] * frequencia
        plt.hist(data, bins = range(1,self.faces+2), density = True, align= 'left', color = 'skyblue', edgecolor = 'black')
        plt.xticks(range(1, self.faces+1))
        plt.xlabel("Face")
        plt.ylabel("Frequência relativa")
        plt.title(f"Frequência relativa de cada face para dado jogado {self.vezes_jogadas} vezes")
        plt.show()

    
    # def grafico_erro(self):




dado1 = Dado_Ideal(6)

for i in range (10):
    print(dado1.jogar_dado(2**i))




