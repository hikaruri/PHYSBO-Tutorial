import mglearn
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import numpy as np

import physbo
import matplotlib.pyplot as plt

def simulator(actions:int) -> float:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    x = alpha_val[actions][0]
    lasso = Lasso(alpha = x).fit(X_train, y_train)
    fx = lasso.score(X_test, y_test)
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
    fig.savefig(Figname) 

if __name__ == '__main__':
    # Make a set of candidates, test_X
    window_num=10001
    alpha_max = 0.1
    alpha_min = 0.0
    alpha_action = []
    fx_action = []
    alpha_val = np.linspace(alpha_min,alpha_max,window_num).reshape(window_num, 1)
    X, y = mglearn.datasets.load_extended_boston()

    policy = physbo.search.discrete.policy(test_X=alpha_val)
    policy.set_seed(10)
    policy.random_search(max_num_probes=3, simulator=simulator)

    for i in range(10):
        policy.bayes_search(max_num_probes=1, simulator=simulator, score="EI", interval=1, num_rand_basis=500)
        Figname = "BO_"+ str(i) + ".png"
        plotfig(policy,alpha_val,Figname)

    #score = policy.get_score(mode="EI", xs=test_X)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {alpha_val[best_actions[-1], :]}")
