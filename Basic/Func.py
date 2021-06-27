import numpy as np

import physbo
import matplotlib.pyplot as plt


def function(x) -> float:
    fx = 0.1 * (2 * x - 1) * (x - 3) * (x - 5)
    return fx


def simulator(actions: int) -> float:
    x = alpha_val[actions][0]
    fx = function(x)
    return fx


def plotfig(policy, X, fx_action,
            alpha_action_val, Figname):
    mean = policy.get_post_fmean(X)
    var = policy.get_post_fcov(X)
    std = np.sqrt(var)

    x = X[:, 0]
    fig, ax = plt.subplots()
    ax.plot(x, mean)
    ax.fill_between(x, (mean-std), (mean+std), color='b', alpha=.1)
    ax.scatter(alpha_action_val, fx_action)
    x1 = np.arange(0, 5, 0.01)
    y1 = function(x1)
    plt.plot(x1, y1, color='#ff4500')
    fig.savefig(Figname)


if __name__ == '__main__':
    # Make a set of candidates, test_X
    window_num = 10001
    alpha_max = 5.0
    alpha_min = 0.0

    alpha_val = np.linspace(alpha_min, alpha_max,
                            window_num).reshape(window_num, 1)

    policy = physbo.search.discrete.policy(test_X=alpha_val)
    policy.set_seed(10)
    res = policy.random_search(max_num_probes=1, simulator=simulator)

    # policy.bayes_search(max_num_probes=10, simulator=simulator,
    #                     score="EI", interval=1, num_rand_basis=500)

    for i in range(10):
        res = policy.bayes_search(max_num_probes=1, simulator=simulator,
                                  score="EI", interval=1, num_rand_basis=i)
        fx_action = [res.fx[i] for i in range(res.total_num_search)]
        alpha_action_val = \
            [alpha_val[res.chosen_actions[i]][0]
                for i in range(res.total_num_search)]

        Figname = "BO_" + str(i) + ".png"
        plotfig(policy, alpha_val, fx_action,
                alpha_action_val, Figname)

    # score = policy.get_score(mode="EI", xs=test_X)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {alpha_val[best_actions[-1], :]}")
