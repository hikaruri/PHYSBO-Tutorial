import numpy as np

import physbo
import matplotlib.pyplot as plt

def simulator(actions:int) -> float:
    x = alpha_val[actions][0]
    fx = 0.1 * ( 2 * x - 1 ) * ( x - 3 ) * ( x - 5 ) 
    alpha_action.append(x)
    fx_action.append(fx)
    return fx

def plotfig(policy, X, Figname):
    mean = policy.get_post_fmean(X)
    var = policy.get_post_fcov(X)
    std = np.sqrt(var)

    x = X[:,0]
    fig, ax = plt.subplots()
    ax.plot(x, mean)
    ax.fill_between(x, (mean-std), (mean+std), color='b', alpha=.1)
    ax.scatter(alpha_action, fx_action)
    x1 = np.arange(0, 5, 0.01)
    y1 = 0.1 * ( 2 * x1 - 1 ) * ( x1 - 3 ) * ( x1 - 5 ) 
    plt.plot(x1, y1, color='#ff4500')
    #plt.show()
    fig.savefig(Figname) 

if __name__ == '__main__':
    # Make a set of candidates, test_X
    window_num=10001
    alpha_max = 5.0
    alpha_min = 0.0
    alpha_action = []
    fx_action = []
    alpha_val = np.linspace(alpha_min,alpha_max,window_num).reshape(window_num, 1)

    policy = physbo.search.discrete.policy(test_X=alpha_val)
    policy.set_seed(10)
    policy.random_search(max_num_probes=1, simulator=simulator)

    for i in range(10):
        policy.bayes_search(max_num_probes=1, simulator=simulator, score="EI", interval=1, num_rand_basis=500)
        Figname = "BO_"+ str(i) + ".png"
        plotfig(policy,alpha_val,Figname)

    #score = policy.get_score(mode="EI", xs=test_X)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {alpha_val[best_actions[-1], :]}")
