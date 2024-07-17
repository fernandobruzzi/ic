import numpy as np
import matplotlib.pyplot as plt

class Dado_Enviesado:
    
    def __init__(self, faces, vies):
        #determina os atributos faces e a frequencia de cada face 
        self.faces = faces
        self.frequencia_das_faces = np.zeros((faces+1,), dtype=int)
        self.vezes_jogadas = 0
        #somamos +1 no vetor que guarda a frequência para fazer com que a face 1 fique na posicao 1 do vetor

        #o nosso vies é uma matrix faces x 2: (face, peso_da_face), sendo o peso um numero entre 0 e 1
        #com isso, determinamos a probabilidade de cada face
        self.p_face = np.zeros((faces+1,2))
        intervalo_ocupado_pelo_vies = 0 
        faces_enviesadas =[]
        for i in vies:
            faces_enviesadas.append(i[0])
            intervalo_ocupado_pelo_vies+= i[1]
        
        p_nao_enviesadas = (1-intervalo_ocupado_pelo_vies)/(faces-len(faces_enviesadas))

        for i in range(1,faces+1):
            j = 0
            if i in faces_enviesadas:
                self.p_face[i] = [self.p_face[i-1][1], self.p_face[i-1][1]+vies[j][1]] 
                j+=1
            else:
                self.p_face[i] = [self.p_face[i-1][1], self.p_face[i-1][1] + p_nao_enviesadas]
        #dessa forma temos o intervalo associado a cada face

        
    def jogar_dado(self, vezes):
        #atualiza quantas vezes o dado já foi jogado no total
        self.vezes_jogadas+= vezes

        #gera os resultados
        resultado = np.random.rand(vezes)
        
        #cria a lista para armazenar os resultados dessa jogada com cada posicao correspondendo a uma face
        resultados_nessa_jogada = np.zeros((self.faces+1,), dtype=int)

        #percorre os resultados e adiciona no historico e nos resultados dessa jogada
        for i in np.nditer(resultado):
            for j in range(1, len(self.p_face)):
                if ((i >= self.p_face[j][0]) and (i <= self.p_face[j][1])):
                    resultados_nessa_jogada[j] += 1
                    self.frequencia_das_faces[j] += 1 


        #podemos fazer o mesmo sorteio utilizando também a funcao random choice do np
        resultado_np = np.random.choice(self.faces+1, vezes, p = [x[1]-x[0] for x in self.p_face])
        resultado_nessa_jogada_np = np.zeros((self.faces+1,), dtype=int) 
        for i in np.nditer(resultado_np):
            resultado_nessa_jogada_np[i]+=1
    

        return (f"Os resultados obtidos pela função implementada foram: {resultados_nessa_jogada[1:]}\n" f"Os resultados obtidos pela função do np foram: {resultado_nessa_jogada_np[1:]}\n"
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


dado1 = Dado_Enviesado(6,[[1,0.9]])

for i in range (10):
    # print(dado1.jogar_dado(2**i))
    dado1.jogar_dado(2**i)

