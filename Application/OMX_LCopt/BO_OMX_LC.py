import numpy as np
import physbo
import matplotlib.pyplot as plt
import subprocess

def simulator(actions: int) -> float:
    Lattice_Constant = float(X[actions][0])
    Lattice_Constant = str(Lattice_Constant)
    line_1 = [Lattice_Constant, ' ', '0.0', ' ', Lattice_Constant, '\n']
    line_2 = [Lattice_Constant, ' ', Lattice_Constant, ' ', '0.0', '\n']
    line_3 = ['0.0', ' ', Lattice_Constant, ' ', Lattice_Constant, '\n']
    with open("omx.in", mode="w") as f:
        f.write('<Atoms.UnitVectors\n')
        f.writelines(line_1)
        f.writelines(line_2)
        f.writelines(line_3)
        f.write('Atoms.UnitVectors>\n')
    subprocess.call(exec_makeinput, shell=True)
    subprocess.call(exec_cmd, shell=True)
    with open("omx.out", 'r') as fpout:
        lines = fpout.readlines()
        Energy = np.nan
        for line in lines:
            if line.find("Utot") >= 0:
                ene = line.split()
                Energy = float(ene[1])
                break
    #Energy = -2 * X[actions][0]
    x_action.append(X[actions][0])
    fx_action.append(-Energy)
    return -Energy

def plotfig(policy, X, Figname):
    mean = policy.get_post_fmean(X)
    var = policy.get_post_fcov(X)
    std = np.sqrt(var)

    x = X[:,0]
    fig, ax = plt.subplots()
    ax.plot(x, mean)
    ax.fill_between(x, (mean-std), (mean+std), color='b', alpha=.1)
    ax.scatter(x_action, fx_action)
    fig.savefig(Figname) 

if __name__ == '__main__':

    exec_makeinput = "cat Cdia.dat >> omx.in"
    exec_cmd = "mpirun -np 6 ~/DFTcodes/VerMKL/openmx3.8/source/openmx omx.in"

    # Make a set of candidates, test_X
    window_num=10001
    x_max = 2.0
    x_min = 1.5
    x_action = []
    fx_action = []

    X = np.linspace(x_min,x_max,window_num).reshape(window_num, 1)
    policy = physbo.search.discrete.policy(test_X=X)
    policy.set_seed(0)
    policy.random_search(max_num_probes=2, simulator=simulator)
    for i in range(10):
        policy.bayes_search(max_num_probes=1, simulator=simulator, score="EI", interval=1, num_rand_basis=i)
        Figname = "BO_"+ str(i) + ".png"
        plotfig(policy,X,Figname)
    #score = policy.get_score(mode="EI", xs=test_X)
    best_fx, best_actions = policy.history.export_sequence_best_fx()
    print(f"best_fx: {best_fx[-1]} at {X[best_actions[-1], :]}")
