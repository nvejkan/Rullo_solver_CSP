# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:22:07 2018

@author: Nattawut Vejkanchana
"""
import numpy as np
from copy import deepcopy

def create_rullo_problem(dim,choice):
    p_zero = np.random.choice(range(30,60))
    p_left = 100-p_zero
    p_each = int(p_left/len(choice))
    p_zero = 100-(p_each*len(choice))
    weight = [p_zero]
    weight.extend([p_each]*len(choice))
    weight = np.array(weight)/100
    
    sol = np.random.choice(a = list(set(choice).union(set([0]))),
                           size=(dim,dim),p=weight)
    prob = deepcopy(sol)
    prob[prob == 0] = np.random.choice(a = choice)
    col_sum = sol.sum(axis=0)
    row_sum = sol.sum(axis=1)
    return prob,sol,row_sum,col_sum

#p1,s1 = create_rullo_problem(5,[2,3,4])
#p1,s1,rs,cs = create_rullo_problem(3,[2,3,4])
    
#np.random.choice([0,2,3,4], p=[0.5,0.2,0.2,0.2], size=(5,5))
#
#p_zero = np.random.choice(range(30,60))
    
#m,sol,row_sum,col_sum = create_rullo_problem(8,range(1,20))
