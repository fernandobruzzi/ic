import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import dirichlet
import random

class Yumi():

    def __init__(self):
        # o dicionario serve para guardar a dinamica do ambiente no formato da funcao p(r,s'|a,s), a ordem dos parametros é 1-s(estado atual), 2-a(acao tomada), 3-s´(proxximo estado), 4-r(recompensa a ser recebida) 
        self.p_dynamics = {'ronronando':{
                                'fazer carinho':{
                                    'ronronando': {
                                            'levar mordida': 0.05, 
                                            'nao levar mordida':0.55}, 
                                    'rosnando': {
                                            'levar mordida': 0.1, 
                                            'nao levar mordida':0.3}
                                            }, 
                                'admirar' : {
                                    'ronronando': {
                                            'levar mordida': 0.01, 
                                            'nao levar mordida':0.9}, 
                                    'rosnando': {
                                            'levar mordida': 0.03, 
                                            'nao levar mordida':0.06}
                                            }
                            },
                           'rosnando' : {
                                'fazer carinho':{
                                    'ronronando': {
                                            'levar mordida': 0.08, 
                                            'nao levar mordida':0.02}, 
                                    'rosnando': {
                                            'levar mordida': 0.8, 
                                            'nao levar mordida':0.1}
                                            }, 
                                'admirar' : {
                                    'ronronando': {
                                            'levar mordida': 0.2, 
                                            'nao levar mordida':0.5}, 
                                    'rosnando': {
                                            'levar mordida': 0.1, 
                                            'nao levar mordida':0.2}
                                            }
                           }
                           }
        self.states = ['ronronando', 'rosnando']
        self.actions = ['fazer carinho','admirar']
        self.rewards = [('levar mordida',-5),('nao levar mordida',1)]



    def policy_eval(self, policy, V_pi, gamma, epsilon = 5.96e-08):
        delta = 1
        steps = 0
        # for v in V_pi: V_pi[v]=1000000 #iniciamos com valor arbitrario
        while delta >= epsilon:
            delta = 0
            for s in self.states:
                v = V_pi[s]
                value = 0
                for a in self.actions:
                    for s_next in self.states:
                        for r in self.rewards:
                            value += policy[s][a]*(self.p_dynamics[s][a][s_next][r[0]] *(r[1] + gamma* V_pi[s_next]))
                V_pi[s] = value
                delta = max(delta, abs(v-V_pi[s]))
            steps+=1
        # print(steps)
        return V_pi
    
    def policy_improvement(self, policy, gamma, V_pi):
        policy_stable = True
        for s in self.states:
            old_policy = policy
            values = []
            for a in self.actions:
                k=0
                for s_next in self.states:
                        for r in self.rewards:
                            k += self.p_dynamics[s][a][s_next][r[0]] *(r[1] + gamma* V_pi[s_next])
                values.append(k)
            #selecao da melhor acao
            if(values[0]==values[1]): policy[s]['fazer carinho'], policy[s]['admirar'] =0.5, 0.5 #checar de isso altera o valor da policy
            else :
                if(values[0] > values [1]): policy[s]['fazer carinho'], policy[s]['admirar'] = 1.0,0.0
                else: policy[s]['fazer carinho'], policy[s]['admirar'] =0.0,1.0
            #por fim checamos se isso alterou a politica
            if(old_policy!=policy):
                policy_stable = False
                
        if policy_stable: return V_pi, policy
        else: self.policy_eval(policy, V_pi,gamma)



    def policy_iteration(self):
        V_pi = {'ronronando':0, 'rosnando':0}
        policy = {
    'ronronando':{
        'fazer carinho': 0,
        'admirar': 0
    },
    'rosnando': {
        'fazer carinho':0,
        'admirar': 0        
    } 
}
        # vamos definir os valores arbitrarios de V_pi e de policy arbitrariamente
        probs = dirichlet((1,1)).rvs(2)
        policy['ronronando']['fazer carinho'], policy['ronronando']['admirar'] = probs[0]
        policy['rosnando']['fazer carinho'], policy['rosnando']['admirar'] = probs[1]
        V_pi['ronronando'], V_pi['rosnando'] = random.uniform(1,100), random.uniform(1,100)
        # gamma=random.uniform(0,1)
        gamma = 0.9
        # realizamos a policy evaluation
        V_pi = self.policy_eval(policy, V_pi, gamma)
        
        V_pi, policy = self.policy_improvement(policy,gamma,V_pi)

        return V_pi, policy


    def value_iteration(self):
        epsilon = 5.96e-08
        # gamma=random.uniform(0,1)
        gamma = 0.9
        V_pi = {'ronronando':0, 'rosnando':0}
        # vamos definir os valores arbitrarios de V_pi
        V_pi['ronronando'], V_pi['rosnando'] = random.uniform(1,100), random.uniform(1,100)

        delta = 1
        while delta >= epsilon:
            delta = 0
            for s in self.states:
                v = V_pi[s]
                values = []
                for a in self.actions:
                    for s_next in self.states:
                            for r in self.rewards:
                                values.append(self.p_dynamics[s][a][s_next][r[0]] *(r[1] + gamma* V_pi[s_next]))
                # print(values)
                V_pi[s] = max(values)
                # print(V_pi)
                delta = max(delta, abs(v-V_pi[s]))
        
        policy = {
                    'ronronando':{
                        'fazer carinho': 0,
                        'admirar': 0
                    },
                    'rosnando': {
                        'fazer carinho':0,
                        'admirar': 0        
    } 
}
        for s in self.states:
            for a in self.actions:
                for s_next in self.states:
                        for r in self.rewards:
                            values.append(self.p_dynamics[s][a][s_next][r[0]] *(r[1] + gamma* V_pi[s_next]))
            if(values[0]==values[1]): policy[s]['fazer carinho'], policy[s]['admirar'] =0.5, 0.5 #checar de isso altera o valor da policy
            else :
                if(values[0] > values [1]): policy[s]['fazer carinho'], policy[s]['admirar'] = 1.0,0.0
                else: policy[s]['fazer carinho'], policy[s]['admirar'] =0.0,1.0

        return policy        




policy1 = {
    'ronronando':{
        'fazer carinho': 0.5,
        'admirar': 0.5
    },
    'rosnando': {
        'fazer carinho':0.05,
        'admirar': 0.95        
    } 
}
V_pi1= {'ronronando':1, 'rosnando':1}

yumi = Yumi()

policy2 = dict()
V_pi2 = dict()
V_pi2, policy2 = yumi.policy_iteration()
print(policy2)

policy3 = dict()
policy3 = yumi.value_iteration()
print(policy3)