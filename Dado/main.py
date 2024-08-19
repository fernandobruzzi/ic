import os
import matplotlib.pyplot as plt
from dado_enviesado import Dado_Enviesado
from dado_ideal import Dado_Ideal

# tem que consertar alguma coisa na parte de pegar o endereco para criar a folder ou a imagem., ou pode ser que rodando no terminal do windows ao inves do wsl funcione melhor   

faces_dado = int(input("Quatas faces tem o dado? \n"))
f = int(input("Qual a face enviesada? \n"))
c = float(input("Como é esse viés? \n"))
vies = [[f, c]]
vezez_jogads = int(input("Quantas vezes voce quer jogar o dado? \n"))
m = int(input("De quantas em quantas vezes voce quer checar o resultado? \n"))
q = bool(input("Voce gostaria de salvar as imagens geradas? \n" ))
e = bool(input("Voce gostaria de ver como as imagens ficam quando vao sendo geradas? \n"))

if q == True:
    i = 1
    while os.path.exists(f'ic/Dado/graph-images/experimento-{i}'):
        i += 1
    new_folder_name = f'ic/Dado/graph-images/experimento-{i}'
    os.makedirs(new_folder_name)
    

dado_normal = Dado_Ideal(faces_dado)
dado_env = Dado_Enviesado(faces_dado, vies=vies)

for i in range(vezez_jogads):
    dado_normal.jogar_dado(2**i)
    dado_env.jogar_dado(2**i)
    if i%m == 0:
        dado_normal.grafico_jogadas()
        plt.savefig(f"{new_folder_name}/dado-normal-jog-{(2**i)+1}vezes.png")
        if e == True and (i+1)%m == 0: plt.show()
        plt.clf()

        dado_normal.grafico_erro()
        plt.savefig(f"{new_folder_name}/dado-normal-erro-{(2**i)+1}vezes.png")
        if e == True and (i+1)%m == 0: plt.show()
        plt.clf()


        dado_normal.grafico_face_monitorada()
        plt.savefig(f"{new_folder_name}/dado-normal-monitor-{(2**i)+1}vezes.png")
        if e == True and (i+1)%m == 0: plt.show()
        plt.clf()

        dado_env.grafico_jogadas()
        plt.savefig(f"{new_folder_name}/dado-env-jog-vies_{c}-{(2**i)+1}vezes.png")
        if e == True and (i+1)%m == 0: plt.show()
        plt.clf()

        dado_env.grafico_erro()
        plt.savefig(f"{new_folder_name}/dado-env-erro-vies_{c}-{(2**i)+1}vezes.png")
        if e == True and (i+1)%m == 0: plt.show()
        plt.clf()

        dado_env.grafico_face_monitorada()
        plt.savefig(f"{new_folder_name}/dado-env-monitor-vies_{c}-{(2**i)+1}vezes.png")
        if e == True and (i+1)%m == 0: plt.show()
        plt.clf()
