#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:29:42 2020

https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf

Exemplo 6.5: Mundo da grade ventoso A Figura 6.10 mostra um mundo da grade padrão, 
com estados de início e objetivo, mas com uma diferença: existe um vento cruzado para cima no meio da grade. 
As ações são as quatro padrão - cima, baixo, direita e esquerda - mas na região central os próximos estados 
resultantes são deslocados para cima por um "vento", cuja força varia de coluna para coluna. 
A força do vento é dada abaixo de cada coluna, em número de células 
deslocadas SG 0 0 0 1 1 1 2 2 1 0 movimentos padrão dos movimentos do rei 
Figura 6.10: Mundo da grade no qual o movimento é alterado por um dependente da localização, ascendente "vento".



341/5000
Exercício 6.6: Mundo da Grade Ventoso com Movimentos do Rei 
Resolva a tarefa do mundo da grade ventoso assumindo oito ações possíveis, 
incluindo os movimentos diagonais, em vez das quatro usuais. 
Quanto melhor você pode fazer com as ações extras? 
Você pode se sair melhor incluindo uma nona ação que não causa nenhum movimento além daquele causado pelo vento?

@author: dgiroto
"""

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import random


class Mundo:
    
    def __init__(self):
         
        self.row = 10 
        self.col = 10
        
        #self.pcardeais = [
        #         'N_',
        #    'O_',     'L_',
        #         'S_']
        #self.actions = [  
        #                 (-1, 0),
        #        (0, -1),          (0, 1),
        #                 (1,  0)
        #    ]
        
        self.pcardeais = [
            'NO','N_','NE',
            'O_',     'L_',
            'SO','S_','SE']
        self.actions = [  
                (-1, -1), (-1, 0), (-1, 1),
                ( 0, -1),          ( 0, 1),
                ( 1,  1), ( 1, 0), ( 1, 1)
            ]
        
        #self.forca_vento_coluna = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
        self.forca_vento_coluna = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
        
        self.grade = [ (row, col) for row in range(self.row) for col in range(self.col)]
        
        self.inicio = (5, 0)
        self.fim =    (5, 7)
        
        self.movimentos = []
        
    def is_inicio(self, posicao):
        return posicao[0] == self.inicio[0] and posicao[1] == self.inicio[1]
    
    def is_fim(self, posicao):
        return posicao[0] == self.fim[0] and posicao[1] == self.fim[1]
    
    def pcardeal_to_action(self, pcardeal):
        indexes = [i for i,x in enumerate(self.pcardeais) if x == pcardeal]
        return self.actions[indexes[0]]
    
    def action_to_pcardeal(self, action):
        indexes = [i for i,x in enumerate(self.actions) if x == action]
        return self.pcardeais[indexes[0]]
        
    def mover(self, origem, movimento):
        
        destino = np.array(origem) + np.array(movimento)
        
        if -1 in list(destino) or self.col in list(destino):
            self.movimentos.append( (None, self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino))  )
            return self.movimentos[-1]
            #return (None, self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino)) 
        
        coluna_destino = destino[1]
        forca_vento = self.forca_vento_coluna[coluna_destino]
        
        if forca_vento > 0:
            for it in range(forca_vento):
                destino = np.array(destino) + np.array(self.pcardeal_to_action('N_'))
                if -1 in list(destino) or self.col in list(destino):
                    self.movimentos.append( (None, self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino)) )
                    return self.movimentos[-1]
                    #return (None, self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino))
        
        self.movimentos.append( (tuple(destino), self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino)) )
        return  self.movimentos[-1]
    
    def limpar_caminho_realizaso(self):
        self.movimentos = []
        
    def caminho_realizaso(self,posicao_inicio):
        
        tmp = [[ '__' for row in range(self.row)] for col in range(self.col)]
        tmp = np.array(tmp)
        tmp[posicao_inicio] = 'i_'
        tmp[self.fim] = 'f_'
        
        
        movs = []
        if len(self.movimentos)>0 :
            for mov in self.movimentos:
                movs.append(mov[1])
                if mov[0] is not None and tmp[mov[0]] !='f_':
                    tmp[mov[0]] = mov[1]
            print(tmp)
        return movs

    def teste(self):
        posicao, movimento, inicio, fim = (self.inicio,'i', True, False)
        for it in range(3):
            posicao, movimento, inicio, fim = self.mover(posicao, self.pcardeal_to_action('S'))
        for it in range(9):
            posicao, movimento, inicio, fim = self.mover(posicao, self.pcardeal_to_action('L'))
        for it in range(8):
            posicao, movimento, inicio, fim = self.mover(posicao, self.pcardeal_to_action('S'))
        for it in range(2):
            posicao, movimento, inicio, fim = self.mover(posicao, self.pcardeal_to_action('O'))
        print(self.caminho_realizaso())

class Cell:
    def __init__(self, actions, row, col):
        self.cell = (row, col)
        self.value = 0
        self.values = [0 for a in actions];
        self.indexActions = -1;
        
    def epsilon_greedy(self, epsilon, actions ):
        p = np.random.random()
        if (p < epsilon):
            action = self.explore(actions)
        else:
            action = self.exploit(actions)   
        
        self.value = self.values[self.indexActions]
        return action  
    
    def exploit(self, actions):
        self.indexActions = self.values.index(max(self.values))
        action = actions[self.indexActions]
        return action
 
    def explore(self, actions):
        action = random.choice(actions);
        self.indexActions = actions.index(action)
        return action
    
    def learn(self, alpha, reward_value, gamma, cell_final_state ):
        #self.value += alpha * (reward_value + gamma * cell_final_state.value - self.value)
        #self.value += alpha * (reward_value + gamma * cell_final_state.values[self.indexActions] - self.value)
        self.value += alpha * (reward_value + gamma * np.max(cell_final_state.values) - self.value)
        self.values[self.indexActions] = self.value

class Rei:
    def __init__(self):
        
        self.gamma = 1.0
        self.reward_value = -1
        self.alpha = 0.5 
        self.epsilon = 0.1 
        self.iterations = 10000
        self.Q = None
    
    def takeAction(self, posicao, action, mundo):
        
        
        #if mundo.is_inicio(tuple(posicao)) or mundo.is_fim(tuple(posicao)):
        if mundo.is_fim(tuple(posicao)):
            return 0, None
        
        nova_posicao, movimento, inicio, fim = mundo.mover(posicao, action)
        #print(mundo.action_to_pcardeal(action))
        #final_state = np.array(state) + np.array(action)
        #print(movimento)
        #saiu do mundo
        if nova_posicao is None or inicio:
            return -100, posicao
        
        return self.reward_value, tuple(nova_posicao)
        
    
    def learn(self, mundo):
        
        deltas = {(row, col):list() for row in range(mundo.row) for col in range(mundo.col)}
        
        tmp = [[Cell(mundo.actions,row,col) for row in range(mundo.row)] for col in range(mundo.col)]
        self.Q = np.array(tmp)
        
        for it in range(self.iterations):
            

            #print(it)
            posicao = tuple(random.choice(mundo.grade))
            #posicao = mundo.inicio
            
            posicao_i = posicao
            
            mundo.limpar_caminho_realizaso()
            
            sub = 0
            while True:
                sub += 1
                
                if sub>1000:
                    break
            
                current_cell = self.Q[posicao]
                
                #print(current_cell)
                
                action = current_cell.epsilon_greedy(self.epsilon, mundo.actions)
                reward, nova_posicao = self.takeAction(posicao, action, mundo)
                
                if nova_posicao is None:
                    break
                
                next_cell =  self.Q[nova_posicao] 
                old_cell_value = current_cell.value
                #Q[s] += alpha * (reward_value + gamma * Q[nova_posicao] - Q[s])
                current_cell.learn(self.alpha, reward, self.gamma, next_cell )
               
                deltas[posicao].append(float(np.abs(old_cell_value - current_cell.value)))
                
                posicao = nova_posicao
                
                #if reward == -1:
                    #print(it)
                #    break
            if it in [1000,5000,9000]:
                print('it = ',it, ' subIt= ',sub)
                print(mundo.caminho_realizaso(posicao_i))
        print('fim.')
        all_series = [list(x)[:50] for x in deltas.values()]
        return all_series
    
    def melhor_caminho(self,posicao_inicio, mundo):

        #posicao = mundo.inicio
        posicao = posicao_inicio
        
        mundo.limpar_caminho_realizaso()
        
        for it in range(20):
            
            current_cell = self.Q[posicao]
            
            #print(current_cell)
            
            action = current_cell.epsilon_greedy(-1, mundo.actions)
            nova_posicao, movimento, inicio, fim = mundo.mover(posicao, action)
            
            if nova_posicao is None or fim:
                break
            
            next_cell =  self.Q[nova_posicao] 
            posicao = nova_posicao
            
        return mundo.caminho_realizaso(posicao_inicio)
        
        
       
#Mundo().teste()      


mundo = Mundo() 
rei = Rei()
melhor_caminho = rei.learn(mundo)

print(rei.melhor_caminho(mundo.inicio, mundo))

plt.figure(figsize=(20,10))
all_series = melhor_caminho
for series in all_series:
    plt.plot(series)

    
