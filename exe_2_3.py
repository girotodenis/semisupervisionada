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
        
        self.cardeais = [
                 'N',
            'O',     'L',
                 'S']
        self.actions = [  
                         (-1, 0),
                (0, -1),          (0, 1),
                         (1,  0)
            ]
        
        #self.cardeais = [
        #    'NO','N','NE',
        #    'O',     'L',
        #    'SO','S','SE']
        #self.actions = [  
        #        (-1, -1), (-1, 0), (-1, 1),
        #        ( 0, -1),          ( 0, 1),
        #        ( 1,  1), ( 1, 0), ( 1, 1)
        #    ]
        
        self.forca_vento_coluna = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
        
        tmp = [[ (row, col) for row in range(self.row)] for col in range(self.col)]
        self.grade = np.array(tmp)
        
        self.inicio = (5, 0)
        self.fim =    (5, 7)
        
    def is_inicio(self, posicao):
        return posicao[0] == self.inicio[0] and posicao[1] == self.inicio[1]
    
    def is_fim(self, posicao):
        return posicao[0] == self.fim[0] and posicao[1] == self.fim[1]
    
    def cardeal_to_action(self, cardeal):
        indexes = [i for i,x in enumerate(self.cardeais) if x == cardeal]
        return self.actions[indexes[0]]
    
    def action_to_cardeal(self, action):
        indexes = [i for i,x in enumerate(self.actions) if x == action]
        return self.cardeais[indexes[0]]
        
    def mover(self, origem, movimento):
        
        destino = np.array(origem) + np.array(movimento)
        
        if -1 in list(destino) or self.col in list(destino):
            return None, self.is_inicio(destino), self.is_fim(destino)
        
        coluna_destino = destino[1]
        forca_vento = self.forca_vento_coluna[coluna_destino]
        
        if forca_vento > 0:
            for it in range(forca_vento):
                destino = np.array(destino) + np.array(self.cardeal_to_action('N'))
                if -1 in list(destino) or self.col in list(destino):
                    return None, self.is_inicio(destino), self.is_fim(destino)
        
        return tuple(destino), self.is_inicio(destino), self.is_fim(destino)


        
m = Mundo()      
caminho = 'L'
print(caminho,' = ', m.cardeal_to_action(caminho))
print('(1,0) = ', m.action_to_cardeal((1,0)))

tmp = [[ '_' for row in range(m.row)] for col in range(m.col)]
tmp = np.array(tmp)
tmp[m.inicio] = 'i'
tmp[m.fim] = 'f'

posicao, inicio, fim = (m.inicio, True, False)

for it in range(3):
    posicao, inicio, fim = m.mover(posicao, m.cardeal_to_action('S'))
    print(posicao)
    tmp[posicao] = 'S'

for it in range(9):
    posicao, inicio, fim = m.mover(posicao, m.cardeal_to_action('L'))
    print(posicao)
    tmp[posicao] ='L'

for it in range(8):
    posicao, inicio, fim = m.mover(posicao, m.cardeal_to_action('S'))
    tmp[posicao] = 'S'
    
for it in range(2):
    posicao, inicio, fim = m.mover(posicao, m.cardeal_to_action('O'))
    tmp[posicao] = 'O'

print(fim)
print(tmp)
