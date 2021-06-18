# Interactive calculation
We carry out to optimize the lattice constant of diamond.

## Code
[Interactive.py](../InteractiveBO/Interactive.py)
[data.txt](../InteractiveBO/data.txt)
[Cdia.dat](../InteractiveBO/Cdia.dat)

## Data Preparation
First, we have to prepare `data.txt` as
```
#LatticeConstant Energy(hartree)
1.5 0
⋮
1.595 0
1.600000 -11.599985159165
1.605 0
⋮
1.655 -11.637227265803
1.66 0
1.665 0
⋮
1.69 0
1.695 0
1.700000 -11.655510296074
1.705 0
1.795 0
1.800000 -11.664748351310
⋮
```
In this situation, We have already obtained the energy at lattice constant is `[1.6, 1.655, 1.7, 1.8]` by OpenMX code.
## Set policy, carry out BO
Load data from `data.txt`
```Python
def load_data():
    A =  np.asarray(np.loadtxt('data.txt', skiprows=1, delimiter=' ') )
    X = A[:,0:1]
    t  = -A[:,1] # BO can search only Maximum value
    return X, t
```
Next, we set calculated IDs.
```Python
X, t = load_data()
calculated_ids = []
for i in range(len(t)):
    if t[i] != 0:
        calculated_ids.append(i)
t_initial = t[calculated_ids]
```
And you can carry out BO as
```Python
policy = physbo.search.discrete.policy(test_X=X, initial_data=[calculated_ids, t_initial])
policy.set_seed(0)
actions = policy.bayes_search(max_num_probes=1, simulator=None, score="EI", interval=1,  num_rand_basis = len(calculated_ids))
print(actions, X[actions])
```
## Run code
This is an example of result.
```Bash
[20, 31, 40, 60]
[11.59998516 11.63722727 11.6555103  11.66474835]
Start the initial hyper parameter searching ...
Done

Start the hyper parameter learning ...
0 -th epoch marginal likelihood -9.516262081824358
50 -th epoch marginal likelihood -9.54328271567966
100 -th epoch marginal likelihood -9.563135882712306
150 -th epoch marginal likelihood -9.579822980125696
200 -th epoch marginal likelihood -9.594787650631439
250 -th epoch marginal likelihood -9.609234212733195
300 -th epoch marginal likelihood -9.624988464291654
350 -th epoch marginal likelihood -9.644931857270409
400 -th epoch marginal likelihood -9.672580080125915
450 -th epoch marginal likelihood -9.709678882402578
500 -th epoch marginal likelihood -9.749448005008674
Done

[70] [[1.85]]
```
We have to make next input file of LC = 1.85 {\AA}. If the calculation is finished, we update `data.txt`.
