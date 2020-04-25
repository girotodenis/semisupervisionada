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

V = np.zeros((4, 4))
V[1,1] = 1


i = np.array((1,1)) + np.array((-1,-1))
V[i[0],i[1]]=3
    
    
