import numpy as np
import matplotlib.pyplot as plt

class Dado_Enviesado:
    
    def __init__(self, faces, vies):
        
        #determina os atributos faces e a frequencia de cada face 
        self.faces = faces
        self.frequencia_das_faces = np.zeros((faces,), dtype=int)
        self.jogadas = 0

        #o nosso vies é uma tupla: (face, peso_da_face)
        self.vies = vies
          
       
        
    def jogar_dado(self, vezes):

        #gera os resultados para um dado viciado
        self.frequencia_das_faces[self.vies[0]-1] += np.around((self.vies[1]*vezes),2)
        vezes_sorteaveis = np.around(((1-self.vies[1]) * vezes),2)
        
        i = 0
        while i < vezes_sorteaveis:
            sorteado = np.random.choice([j for j in range(1, self.faces + 1) if j!= self.vies[0]])
            self.frequencia_das_faces[sorteado-1] += 1
            i+=1
        
        
        #gera os dados para construcao do histograma e constroi o histograma

        data = []
        for face, frequencia in enumerate(self.frequencia_das_faces):
            data+= [face+1] * frequencia
        plt.hist(data, bins = range(1,self.faces+2), density = True, align= 'left', color = 'skyblue', edgecolor = 'black')
        plt.xticks(range(1, self.faces+1))
        plt.xlabel("Face")
        plt.ylabel("Frequência relativa")
        plt.title("Frequência relativa de cada face para dado jogado 2^n - 1  vezes")


        return (f"E o historico dos resultados é {self.frequencia_das_faces}")         


dado1 = Dado_Enviesado(6,[1,0.5])

for i in range (12):
    print(dado1.jogar_dado(2**i))
    plt.show()