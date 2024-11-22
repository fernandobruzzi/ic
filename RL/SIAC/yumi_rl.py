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
 



    def policy_eval(self, policy, V_pi, gamma, valor_real = True, epsilon = 5.96e-08):
        
        # nao queremos alterar o valor do parametro por isso fazemos uma copia
        V_pi_copia = V_pi.copy()

        # guardamos o valor de um estado cada iteração
        value_state = []
        value_state.append(V_pi_copia['ronronando'])
        
        delta = 1
        steps = 0
        # for v in V_pi: V_pi[v]=1000000 #iniciamos com valor arbitrario
        while delta >= epsilon:
            delta = 0
            for s in self.states:
                v = V_pi_copia[s]
                value = 0
                for a in self.actions:
                    for s_next in self.states:
                        for r in self.rewards:
                            value += policy[s][a]*(self.p_dynamics[s][a][s_next][r[0]] *(r[1] + gamma* V_pi_copia[s_next]))
                
                V_pi_copia[s] = value
                if((s == self.states[0]) and (valor_real==False)):
                   value_state.append(value)

                delta = max(delta, abs(v-V_pi_copia[s]))
            steps+=1
        
        # print("steps é ", steps)
        if(valor_real): return V_pi_copia
        else: return value_state

    
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
               
        if policy_stable: return V_pi, policy, True
        else: return V_pi, policy, False



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
        V_pi['ronronando'], V_pi['rosnando'] = random.uniform(-100000, 100000), random.uniform(-100000, 100000)
        # gamma=random.uniform(0,1)
        gamma = 0.9
        # realizamos a policy evaluation
        steps = 0
        ready = False
        V_pi = self.policy_eval(policy, V_pi, gamma)
        V_pi, policy, ready  = self.policy_improvement(policy,gamma,V_pi)
        steps +=1
        
        while(ready!=True):
            V_pi = self.policy_eval(policy, V_pi, gamma)
            V_pi, policy = self.policy_improvement(policy,gamma,V_pi)
            steps+=1
        print(steps)
        V_pi = self.policy_eval(policy, V_pi, gamma)
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



def p_eval_results(path, log_scale,gamma, sample_num):
    yumi = Yumi()

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
    # vamos definir os valores arbitrarios de V_pi e de policy aleatoriamente
    probs = dirichlet((1,1)).rvs(2)
    policy['ronronando']['fazer carinho'], policy['ronronando']['admirar'] = probs[0]
    policy['rosnando']['fazer carinho'], policy['rosnando']['admirar'] = probs[1]
    V_pi['ronronando'], V_pi['rosnando'] = random.uniform(-100000, 100000), random.uniform(-100000, 100000)
    # V_pi['ronronando'], V_pi['rosnando'] = random.uniform(0, 100), random.uniform(0, 100)
    # gamma=random.uniform(0,1)
    # gamma = 0.9

    # achamos primeiro o valor real de um estado de acordo com uma política pi, vamos escolher o primeiro estado "ronronando"
    real_value = yumi.policy_eval(policy, V_pi,gamma, True)['ronronando']
    # real_value = yumi.policy_eval(policy, V_pi,gamma, True, epsilon=0.001)['ronronando']
    vector_values = []
    i = 0
    max_len = 0
    while i < sample_num:
    # while i < 10:
        V_pi['ronronando'], V_pi['rosnando'] = random.uniform(-100000, 100000), random.uniform(-100000, 100000)
        # V_pi['ronronando'], V_pi['rosnando'] = random.uniform(0, 100), random.uniform(0, 100)
        
        vector_values.append(yumi.policy_eval(policy,V_pi,gamma,False))
        # vector_values.append(yumi.policy_eval(policy,V_pi,gamma,False,epsilon=0.001))
        if(len(vector_values[i])>max_len): max_len = len(vector_values[i])
        i+=1
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("Steps")
    ax.set_ylabel("Value of state ronronando")
    if(log_scale):
        ax.set_xscale('log') 

    
    ax.set_title("Policy evaluation converge for a single state")
    

    linspace = np.arange(0, max_len+1, step=1)
    real_value = [real_value]*(max_len + 1)
    ax.plot(linspace, real_value,label = f"State 'ronronando' real value", color = 'red', linestyle= '--', alpha=0.8)

    for i in range(len(vector_values)):
        linspace = np.arange(0, len(vector_values[i]), step=1)
        random_color = (random.random(),random.random(),random.random())
        ax.plot(linspace, vector_values[i],label = f"Random value {i+1}", color = random_color, linestyle= 'solid')
    
    fig.savefig(path, format='png')
    return

yumi = Yumi()
V_pi2, policy2 = yumi.policy_iteration()
print(V_pi2,policy2) #gamma = 0.9

# gamma = 0.9
# sample_num = 10
# log_scale = True
# path = f'ic/RL/SIAC/graficos/policy_eval_conv_log_scale={log_scale}_sample_num={sample_num}_gamma={gamma}_epsilon={5.96e-08}.png'
# p_eval_results(path, log_scale=log_scale, gamma=gamma, sample_num=sample_num)

# gamma = 0.9
# sample_num = 10
# log_scale = True
# path = f'ic/RL/SIAC/graficos/policy_eval_conv_log_scale={log_scale}_sample_num={sample_num}_gamma={gamma}_epsilon={5.96e-08}.png'
# p_eval_results(path, log_scale=log_scale, gamma=gamma, sample_num=sample_num)

# gamma = 0.9
# sample_num = 10
# log_scale = False
# path = f'ic/RL/SIAC/graficos/policy_eval_conv_log_scale={log_scale}_sample_num={sample_num}_gamma={gamma}_epsilon={5.96e-08}.png'
# p_eval_results(path, log_scale=log_scale, gamma=gamma, sample_num=sample_num)

# gamma = 0.5
# sample_num = 10
# log_scale = False
# path = f'ic/RL/SIAC/graficos/policy_eval_conv_log_scale={log_scale}_sample_num={sample_num}_gamma={gamma}_epsilon={5.96e-08}.png'
# p_eval_results(path, log_scale=log_scale, gamma=gamma, sample_num=sample_num)


# gamma = 0.9
# sample_num = 100
# log_scale = True
# path = f'ic/RL/SIAC/graficos/policy_eval_conv_log_scale={log_scale}_sample_num={sample_num}_gamma={gamma}_epsilon={5.96e-08}.png'
# p_eval_results(path, log_scale=log_scale, gamma=gamma, sample_num=sample_num)


    
# policy1 = {
#     'ronronando':{
#         'fazer carinho': 0.5,
#         'admirar': 0.5
#     },
#     'rosnando': {
#         'fazer carinho':0.05,
#         'admirar': 0.95        
#     } 
# }
# V_pi1= {'ronronando':1, 'rosnando':1}

# yumi = Yumi()

# policy2 = dict()
# V_pi2 = dict()
# V_pi2, policy2 = yumi.policy_iteration()
# print(V_pi2,policy2)
# print(policy2)

# policy3 = dict()
# policy3 = yumi.value_iteration()
# print(policy3)