import numpy as np

import physbo
import matplotlib.pyplot as plt
import random

def simulator(actions:int) -> float:
    return np.sum(test_X[actions,:])

if __name__ == '__main__':
    # Make a set of candidates, test_X
    # Length of array
    N = 10
    X = []
    for i in range(2**N):
        Gene = []
        for j in range(N):
            if ((i >> j) & 1):
                Gene.append(1)
            else:
                Gene.append(0)
        X.append(Gene)
    test_X = np.array(random.sample(X,len(X)))

    policy = physbo.search.discrete.policy(test_X=test_X)
    policy.set_seed(10)
    policy.random_search(max_num_probes=3, simulator=simulator)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {test_X[best_actions[-1]]}")
    policy.bayes_search(max_num_probes=10, simulator=simulator, score="EI", 
    interval=1, num_rand_basis=500)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {test_X[best_actions[-1]]}")