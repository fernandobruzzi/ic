import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random

class KArmedBandits():

    def __init__(self,k, q_inicial, epslon, alpha):
        # somamos k+1 para termos nossa indexacao comecando em 1, nao vamos usar o indice 0
        self.q=np.full(k+1, q_inicial, dtype=float)
        self.Q= np.full(k+1,0,dtype=float)
        self.N = np.full(k+1,0,dtype=int)
        self.epslon = epslon
        self.alpha = alpha
        self.k = k

    def loop(self, steps, r):
        
        i = 1
        while(i<=steps):
            # a cada jogada temos que adicionar uma amostra de uma distribuicao normal com emdia zero e desvio padrao 0.01 a q
            for a in range(1, self.k+1):
                self.q[a] += norm.rvs(loc=0, scale=0.01)

            p = random.uniform(0,1) #decidimos se seremos gulosos ou nao
            if(p<=self.epslon): #se numero sorteado cair no intervalo [0, epsilon] não somos gulosos
                A = random.randint(1,self.k)
            else: #somos gulosos
                A = np.argmax(self.Q[1:])
                A+=1 #somamos mais 1 já que pegamos o indice do elemetno maximo de self.Q comecando em self.Q[1]
            
            
            R = norm.rvs(loc=self.q[A],scale=0.4)
            
            r[i] = r[i-1] + (1/i+1)*(R-r[i-1]) #fazer a media das recompensas 
            self.N[A]+=1

            if((self.alpha <= 1 ) or (self.alpha>=0)): #fazemos que quando alpha esta fora do intervalo de 0 a 1 estamos no caso de step size de media das recompensas anteriores
                self.Q[A] += (self.alpha)*(R - self.Q[A])
            else: 
                self.Q[A] += (1/self.N[A])*(R - self.Q[A])
            
            i+=1

    
    
def graph_gen(eps, alpha, k, qin, n):
        
        #grafico para comparar cada nivel de greedy com alpha estacionario
        figavgreward= plt.figure()
        ax = figavgreward.add_subplot()
        ax.set_xlabel("Steps")
        ax.set_xscale('log')
        ax.set_ylabel("Reward")
        ax.set_title("Average Reward over Time")
        
        
        for e in eps:
            band = KArmedBandits(k,qin,e,alpha)
            rwds= np.empty(n+1)
            rwds[0]=0
            band.loop(n, rwds)
            random_color = np.random.rand(3,)
            
            # ax.plot(np.arange(n), rwds[1:], label = f"greedy {e}", color = random_color, linestyle= '--', alpha=0.8) aqui é sem dar um smooth
            window_size = 50
            smoothed_rwds = moving_average(rwds,window_size)
            ax.plot(np.arange(len(smoothed_rwds)), smoothed_rwds, label = f"greedy {e}", color = random_color, linestyle= '--', alpha=0.8)
        
        ax.legend()

        figavgreward.savefig(f"ic/RL/ch_2/average_reward_plot_alpha={alpha}.png", format='png')


def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

eps = [0.0, 0.01, 0.1]
arralpha = [0.4,0.8, 2]
k=10
n=5000
for alpha in arralpha:
    graph_gen(eps,alpha,k,5, n)