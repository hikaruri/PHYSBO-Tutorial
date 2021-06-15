# Basic Tutorial
Solving basic problem by PHYSBO
## OneMax Problem
### What is an OneMax problem?
This is the benchmark problem of evolutionary algorithm. The problem is the very simple,
"What is the binary number's array to maximize the function?"
This function is defined as the summation of all elements.
The answer is very simple, all elements are 1.

We will find this answer automatically by BO.

- J.D. Schaffer and L.J. Eshelman. "On crossover as an evolutionary viable strategy". In R.K. Belew and L.B. Booker, editors. Proceedings of the 4th International Conference on Genetic Algorithms, pages 61-68, Morgan Kaufmann, 1991.
- [The OneMax Problem](https://tracer.lcc.uma.es/problems/onemax/onemax.html#SE91)
- [遺伝的アルゴリズムでOneMax問題を解いてみる](https://qiita.com/pontyo4/items/a986df2582f3d0aaaa40)


### Preparation
Generate binary number's array
```Python
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
```
Set test_X as **numpy's array format, ndarray**
```Python
test_X = np.array(random.sample(X,len(X)))
```
### Using PHYSBO

## Searching Maximum value of function
## Interactive calculation
