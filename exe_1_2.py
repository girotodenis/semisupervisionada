# -*- coding: utf-8 -*-
"""

Implemente no exemplo de TD(0) uma estratégia epsilon-greedy, ao invés de uma escolha aleatória de ações. Para decidir qual a ação greedy em um determinado momento, é necessário considerar a maior função de valor nas redondezas de um estado.
Faça experimentos variando o epsilon. Compare os resultados da política greedy após 10, 100, 500 e 1000 episódios, em cada um dos cenários.
Compare esses resultados com os resultados de uma política greedy após 10, 100, 500 e 1000 episódios considerando o código original de exemplo.
Responda com base nos experimentos e plots apresentados: qual o impacto do fator de exploração do agente ao usar o TD(0)?
"""

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import random


# parameters
gamma = 0.1 # discounting rate
reward_value = -1
grid_size = 4
alpha = 0.1 # (0,1] // stepSize
terminal_states = [[0,0], [grid_size-1, grid_size-1]]
actions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
iterations = 10000

V = np.zeros((grid_size, grid_size))
returns = {(i, j):list() for i in range(grid_size) for j in range(grid_size)}
deltas = {(i, j):list() for i in range(grid_size) for j in range(grid_size)}
states = [[i, j] for i in range(grid_size) for j in range(grid_size)]

def generateInitialState():
    initial_state = random.choice(states[1:-1])
    return tuple(initial_state)

def generateNextAction():
    return random.choice(actions)

def takeAction(state, action):
    if list(state) in terminal_states:
        return 0, None
    final_state = np.array(state) + np.array(action)
    if -1 in list(final_state) or grid_size in list(final_state):
        final_state = state
    return reward_value, tuple(final_state)

for it in range(iterations):
    initial_state = generateInitialState()

   # if it in [0, 1, 2, 9, 99, iterations-1]:
   #     print("\nIteration {}".format(it))
   #     print(V)
   #     print("")
        
    while True:
        action = generateNextAction()
        reward, final_state = takeAction(initial_state, action)
        
        if final_state is None:
            break
        
        before =  V[initial_state]
        V[initial_state] += alpha * (reward + gamma * V[final_state] - V[initial_state])
        deltas[initial_state].append(float(np.abs(before - V[initial_state])))
        
        initial_state = final_state

        
plt.figure(figsize=(20,10))
all_series = [list(x)[:50] for x in deltas.values()]
for series in all_series:
    plt.plot(series)