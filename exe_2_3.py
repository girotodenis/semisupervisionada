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
        
        self.pcardeais = [
                 'N',
            'O',     'L',
                 'S']
        self.actions = [  
                         (-1, 0),
                (0, -1),          (0, 1),
                         (1,  0)
            ]
        
        #self.pcardeais = [
        #    'NO','N','NE',
        #    'O',     'L',
        #    'SO','S','SE']
        #self.actions = [  
        #        (-1, -1), (-1, 0), (-1, 1),
        #        ( 0, -1),          ( 0, 1),
        #        ( 1,  1), ( 1, 0), ( 1, 1)
        #    ]
        
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
        
        coluna_destino = destino[1]
        forca_vento = self.forca_vento_coluna[coluna_destino]
        
        if forca_vento > 0:
            for it in range(forca_vento):
                destino = np.array(destino) + np.array(self.pcardeal_to_action('N'))
                if -1 in list(destino) or self.col in list(destino):
                    self.movimentos.append( (None, self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino)) )
                    return self.movimentos[-1]
        
        self.movimentos.append( (tuple(destino), self.action_to_pcardeal(movimento), self.is_inicio(destino), self.is_fim(destino)) )
        return  self.movimentos[-1]
    
    def limpar_caminho_realizaso(self):
        self.movimentos = []
        
    def caminho_realizaso(self):
        tmp = [[ '_' for row in range(self.row)] for col in range(self.col)]
        tmp = np.array(tmp)
        tmp[self.inicio] = 'i'
        tmp[self.fim] = 'f'
        movs = []
        for mov in self.movimentos:
            movs.append(mov[1])
            tmp[mov[0]] = mov[1]
        print(tmp)
        return movs, self.movimentos[-1][3]

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



class Rei:
    def __init__(self):
        
        self.gamma = 0.1 
        self.reward_value = -1
        self.alpha = 0.1 
        self.epsilon = 0.1 
        self.iterations = 1000
        
        
    def learn(self, mundo):
        
        deltas = {(row, col):list() for row in range(mundo.row) for col in range(mundo.col)}
        
        for it in range(self.iterations):

            s = tuple(random.choice(mundo.grade))
            
            
            
           
    
        
       # all_series = [list(x)[:50] for x in deltas.values()]
        return mundo.caminho_realizaso(), []#all_series
        
        
       
#Mundo().teste()      


mundo = Mundo() 
rei = Rei()
melhor_caminho = rei.learn(mundo)
print(melhor_caminho[0])

plt.figure(figsize=(20,10))
all_series = melhor_caminho[1]
for series in all_series:
    plt.plot(series)