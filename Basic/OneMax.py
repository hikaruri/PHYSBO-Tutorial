import numpy as np

import physbo
import matplotlib.pyplot as plt
import random


def simulator(actions: int) -> float:
    return np.sum(X[actions, :])


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
    X = np.array(random.sample(X, len(X)))

    policy = physbo.search.discrete.policy(test_X=X)

    # Random search
    policy.set_seed(10)
    policy.random_search(max_num_probes=3, simulator=simulator)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {X[best_actions[-1]]}")

    # Bayes_search
    res = policy.bayes_search(max_num_probes=20, simulator=simulator,
                              score="EI", interval=1, num_rand_basis=500)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {X[best_actions[-1]]}")

    fig = plt.figure()
    plt.plot(res.fx[0:res.total_num_search])
    best_fx, best_action = res.export_all_sequence_best_fx()
    plt.plot(best_fx)
    fig.savefig("Search.png")

    # Visualization EI
    # policy.bayes_search(max_num_probes=3, simulator=simulator, score="EI",
    #                     interval=1, num_rand_basis=500)
    # print(f"best_fx: {best_fx[-1]} at {test_X[best_actions[-1]]}")
    # scores = policy.get_score(mode="EI", xs=test_X)
    # fig = plt.figure()
    # plt.plot(scores)
    # fig.savefig("EI_1.png")
    # policy.bayes_search(max_num_probes=7, simulator=simulator, score="EI",
    #                     interval=1, num_rand_basis=500)
    # scores = policy.get_score(mode="EI", xs=X)
    # fig = plt.figure()
    # plt.plot(scores)
    # fig.savefig("EI_2.png")
