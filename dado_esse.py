import numpy as np

class Dado:
    
    def __init__(self, faces):
        
        self.faces = faces
        self.historico_de_resultados = np.zeros((faces,), dtype=int)
       
        
    def jogar_dado(self, vezes):
        
        resultado = np.random.randint(1, self.faces + 1, vezes)
        resultados_nessa_jogada = np.zeros((self.faces,), dtype=int)
        
        for i in np.nditer(resultado):
            resultados_nessa_jogada[i - 1]+= 1
            self.historico_de_resultados[i - 1]+=1
        
            
        return (f"Os resultados obtidos foram: {resultados_nessa_jogada}\n"
    f"E a diferenca entre a face que apareceu mais vezes e a que apareceu menos vezes é {resultados_nessa_jogada.max() - resultados_nessa_jogada.min()}\n"
    f"E o historico dos resultados é {self.historico_de_resultados}")


dado1 = Dado(6)

for i in range (20):
    print(dado1.jogar_dado(2**i))
