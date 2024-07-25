import numpy as np
import matplotlib.pyplot as plt

class Dado_Enviesado:
    
    def __init__(self, faces, vies):
        #determina os atributos faces e o historico de cada face 
        self.faces = faces
        self.historico_das_faces = np.zeros((1,faces+1))
        self.vezes_jogadas = np.zeros((1), dtype = int)
        self.link_freq_jog = 0 #esse link serve para relacionar historico[link][x] com jogadas[link]

        #sorteamos uma face para monitorar
        self.face_monitorada = np.random.randint(1, faces + 1)   
        self.contador_face_monitorada = 0
        self.vetor_face_monitorada = []

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
        self.vezes_jogadas = np.append(self.vezes_jogadas, [self.vezes_jogadas[self.link_freq_jog] + vezes])

        #gera os valores do sorteio para serem usados como resultado
        resultado = np.random.rand(vezes)
        
        #cria a lista para armazenar os resultados dessa jogada com cada posicao correspondendo a uma face
        resultados_nessa_jogada = np.zeros((self.faces+1,), dtype=int)

        #percorre os resultados e adiciona no historico e nos resultados dessa jogada
        for i in np.nditer(resultado):
            for j in range(1, len(self.p_face)):
                if ((i >= self.p_face[j][0]) and (i <= self.p_face[j][1])):
                    resultados_nessa_jogada[j] += 1

                    self.contador_face_monitorada+=1
                    if j == self.face_monitorada:
                        self.vetor_face_monitorada+= [self.contador_face_monitorada]
                        self.contador_face_monitorada = 0
                        

        self.historico_das_faces = np.append(self.historico_das_faces,[self.historico_das_faces[self.link_freq_jog] + resultados_nessa_jogada],axis=0)  

        #podemos fazer o mesmo sorteio utilizando também a funcao random choice do np
        resultado_np = np.random.choice(self.faces+1, vezes, p = [x[1]-x[0] for x in self.p_face])
        resultado_nessa_jogada_np = np.zeros((self.faces+1,), dtype=int) 
        for i in np.nditer(resultado_np):
            resultado_nessa_jogada_np[i]+=1

        self.link_freq_jog+=1
        return (f"Os resultados obtidos pela função implementada foram: {resultados_nessa_jogada[1:]}\n" f"Os resultados obtidos pela função do np foram: {resultado_nessa_jogada_np[1:]}\n"
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
        for i in range(self.faces):
            plt.plot(x, ((y[:, i])-(self.p_face[i+1][1]-self.p_face[i+1][0])), label = f"face{i+1}")

        #alem disso, vamos inserir retas para ver qual se adequa ao erro
        plt.plot(x,1/x, label = "1/x")
        plt.plot(x,1/(x**2), label = "1/x**2")
        plt.plot(x,1/np.log(x), label = "1/ln(x)")
        plt.plot(x, 1/x*(np.log(x)), label = "1/x*ln(x)")

        plt.xlabel("Vezes jogadas")
        plt.ylabel("Frequencia real da face - frequencia ideal")
        plt.legend()
        plt.show()

    def media_face_monitorada(self):
        # problema quando a face escolhida aparece na primeira vez
        try:
            media = (sum(self.vetor_face_monitorada))/len(self.vetor_face_monitorada)
            return (f"Devemos fazer aproximadamente {media} lançamentos para que a face {self.face_monitorada} apareça ao menos uma vez")
        except ZeroDivisionError:
            return(f"A face {self.face_monitorada} ainda não apareceu para {sum(self.vezes_jogadas)} jogadas")



dado1 = Dado_Enviesado(4,[1, 0.25])
for i in range (10):
    # print(dado1.jogar_dado(2**i))
    dado1.jogar_dado(2**i)
# dado1.grafico_erro()
print(dado1.media_face_monitorada())


