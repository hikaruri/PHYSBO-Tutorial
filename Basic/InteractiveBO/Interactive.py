import numpy as np

import physbo
import matplotlib.pyplot as plt
import random

def load_data():
    A =  np.asarray(np.loadtxt('data.txt', skiprows=1, delimiter=' ') )
    X = A[:,0:1]
    t  = -A[:,1] # BO can search only Maximum value
    return X, t

X, t = load_data()
calculated_ids = []
for i in range(len(t)):
    if t[i] != 0:
        calculated_ids.append(i)
t_initial = t[calculated_ids]
print(calculated_ids)
print(t_initial)

# Bayes_search
policy = physbo.search.discrete.policy(test_X=X, initial_data=[calculated_ids, t_initial])
policy.set_seed(0)
actions = policy.bayes_search(max_num_probes=1, simulator=None, score="EI", interval=1,  num_rand_basis = 500)
print(actions, X[actions])
