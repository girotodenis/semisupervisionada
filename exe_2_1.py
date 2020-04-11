#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:29:42 2020

@author: dgiroto
"""

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import random

def generateInitialState(states):
    initial_state = random.choice(states[1:-1])
    return tuple(initial_state)
           

def takeAction(state, action, terminal_states, grid_size):
    if list(state) in terminal_states:
        return None
    final_state = np.array(state) + np.array(action)
    if -1 in list(final_state) or grid_size in list(final_state):
        final_state = state
    return tuple(final_state)

class Cell:
    def __init__(self, actions, row, col):
        self.cell = (row, col)
        self.value = 0
        self.values = [0 for a in actions];
        self.indexActions = -1;
        
    def epsilon_greedy(self, epsilon, actions ):
        p = np.random.random()
        if (p < epsilon):
            return self.explore(actions)
        else:
            return self.exploit(actions)   
    
    def exploit(self, actions):
        self.indexActions = self.values.index(max(self.values))
        action = actions[self.indexActions]
        return action
 
    def explore(self, actions):
        action = random.choice(actions);
        self.indexActions = actions.index(action)
        return action
    
    def learn(self, alpha, reward_value, gamma, cell_final_state ):
        self.value += alpha * (reward_value + gamma * cell_final_state.value - self.value)
        self.values[self.indexActions] = self.value
        
    def __str__(self):
        return "cell:{0} value: {1}, top: {2}, down: {3}, right: {4}, left: {5}".format(self.cell, self.value, self.values[0], self.values[1],self.values[2],self.values[3])


def sarsa(epsilon = 0.1, iterations = 1000):
    
    # parameters
    gamma = 0.1 
    reward_value = -1
    grid_size = 4
    alpha = 0.1 
    terminal_states = [[0,0], [grid_size-1, grid_size-1]]
    actions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    
    tmp = [[Cell(actions,row,col) for row in range(grid_size)] for col in range(grid_size)]
    Q = np.array(tmp)
    #Q = np.zeros((grid_size, grid_size))
    
    returns = {(i, j):list() for i in range(grid_size) for j in range(grid_size)}
    deltas = {(i, j):list() for i in range(grid_size) for j in range(grid_size)}
    states = [[i, j] for i in range(grid_size) for j in range(grid_size)]
    values = [0,0,0,0]

    for it in range(iterations):
        s = generateInitialState(states)

            
        while True:
            
            current_cell = Q[s]
            
            #print(current_cell)
            
            action = current_cell.epsilon_greedy(epsilon, actions)
            final_state = takeAction(s, action, terminal_states, grid_size)
            
            if final_state is None:
                break
            
            next_cell =  Q[final_state]
            old_cell_value = current_cell.value
            #Q[s] += alpha * (reward_value + gamma * Q[final_state] - Q[s])
            current_cell.learn(alpha, reward_value, gamma, next_cell )
           
            deltas[s].append(float(np.abs(old_cell_value - current_cell.value)))
            
            s = final_state
    
    all_series = [list(x)[:50] for x in deltas.values()]
    return all_series

        
plt.figure(figsize=(20,10))
all_series = sarsa()#[list(x)[:50] for x in deltas.values()]
for series in all_series:
    plt.plot(series)
