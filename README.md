### Flexible Process Planning

##### Reference: 

##### [1] Luo K. A sequence learning harmony search algorithm for the flexible process planning problem[J]. International Journal of Production Research, 2022, 60(10): 3182-3200.

##### [2] Luo K, Sun J, Guo L. Network-based integer programming models for flexible process planning[J]. International Journal of Production Research, 2022: 1-15.

##### [3] Luo K, Shen G, Li L, et al. 0-1 mathematical programming models for flexible process planning[J]. European Journal of Operational Research, 2022.

-------------

#### The Sequence Learning Harmony Search for Flexible Process Planning (SLHS.py)

| Variables | Meaning                                           |
| --------- | ------------------------------------------------- |
| hms       | Population size                                   |
| iter      | Iteration number                                  |
| pc        | Crossover probability                             |
| min_beta  | The lower bound of scaling factor                 |
| max_beta  | The upper bound of scaling factor                 |
| lb        | The lower bound (list)                            |
| ub        | The upper bound (list)                            |
| pop       | The set of individuals (list)                     |
| score     | The score of individuals (list)                   |
| dim       | Dimension                                         |
| gbest     | The score of the global best individual           |
| gbest_ind | The position of the global best individual (list) |
| iter_best | The global best score of each iteration (list)    |
| con_iter  | The last iteration number when "gbest" is updated |

##### Example

![](https://github.com/Xavier-MaYiMing/Flexible-Process-Planning/blob/main/Example%201.png)

```python
if __name__ == '__main__':
    class Specification:
        def __init__(self, alternative, prior, machine, tool, direction):
            self.alternative = alternative
            self.prior = prior
            self.machine = machine
            self.tool = tool
            self.direction = direction


    # Example 1
    muc = {'m1': 70, 'm2': 35, 'm3': 10, 'm4': 40, 'm5': 85}
    tuc = {'t1': 10, 't2': 10, 't3': 10, 't4': 12, 't5': 8, 't6': 16, 't7': 3, 't8': 3, 't9': 4, 't10': 2, 't11': 10, 't12': 5, 't13': 6, 't14': 3, 't15': 6, 't16': 3, 't17': 4}
    mcc = 150
    tcc = 20
    scc = 90
    operations = {
        1: ['o1a', 'o1b'],
        2: ['o2a', 'o2b'],
        3: ['o3a', 'o3b'],
        4: ['o4'],
        5: ['o5'],
        6: ['o6'],
        7: ['o7'],
        8: ['o8'],
        9: ['o9'],
        10: ['o10'],
        11: ['o11'],
        12: ['o12'],
        13: ['o13a', 'o13b']
    }
    s1 = Specification(['o1b'], [], ['m1', 'm2'], ['t1', 't3'], ['+z'])
    s2 = Specification(['o1a'], ['o2a', 'o2b', 'o13a', 'o13b'], ['m4', 'm5'], ['t5', 't15'], ['+z'])
    s3 = Specification(['o2b'], [], ['m1', 'm2'], ['t1', 't2', 't3', 't4'], ['+z'])
    s4 = Specification(['o2a'], [], ['m4', 'm5'], ['t5'], ['+z'])
    s5 = Specification(['o3b'], [], ['m1', 'm2'], ['t4'], ['-y', '+y'])
    s6 = Specification(['o3a'], [], ['m4', 'm5'], ['t11'], ['-z', '+x'])
    s7 = Specification([], [], ['m1', 'm2'], ['t1', 't2', 't4'], ['-z'])
    s8 = Specification([], ['o4'], ['m1', 'm2'], ['t15'], ['-z'])
    s9 = Specification([], ['o1a', 'o1b', 'o4'], ['m1', 'm2', 'm3', 'm4', 'm5'], ['t10'], ['-z'])
    s10 = Specification([], ['o1a', 'o1b', 'o4', 'o6'], ['m1', 'm2', 'm3', 'm5'], ['t14'], ['-z'])
    s11 = Specification([], ['o1a', 'o1b', 'o4', 'o7'], ['m1', 'm2'], ['t3'], ['-z'])
    s12 = Specification([], [], ['m1', 'm2', 'm3', 'm4', 'm5'], ['t10'], ['-z'])
    s13 = Specification([], ['o9'], ['m1', 'm2', 'm4', 'm5'], ['t14'], '-z')
    s14 = Specification([], ['o10'], ['m1', 'm2'], ['t3'], ['-z'])
    s15 = Specification([], ['o6', 'o7', 'o8'], ['m1', 'm2'], ['t1', 't2', 't3', 't4'], ['-z'])
    s16 = Specification(['o13b'], [], ['m1', 'm2'], ['t1', 't2', 't3', 't4'], ['+z'])
    s17 = Specification(['o13a'], [], ['m4', 'm5'], ['t5'], ['+z'])
    specifications = {'o1a': s1, 'o1b': s2, 'o2a': s3, 'o2b': s4, 'o3a': s5, 'o3b': s6, 'o4': s7, 'o5': s8, 'o6': s9, 'o7': s10, 'o8': s11, 'o9': s12, 'o10': s13, 'o11': s14, 'o12': s15, 'o13a': s16, 'o13b': s17}
    print(main(operations, specifications, muc, tuc, mcc, tcc, scc, 10, 10000))
```

##### Output:

![](https://github.com/Xavier-MaYiMing/Flexible-Process-Planning/blob/main/convergence%20curve.png)

The SLHS converges at its 1,365-th iteration, and the global best value is 833. 

```python
{
  'best score': 833, 
  'best solution': [
    ['o3a', 'm2', 't4', '-y'], 
    ['o1a', 'm2', 't1', '+z'], 
    ['o13a', 'm2', 't1', '+z'], 
    ['o2a', 'm2', 't1', '+z'], 
    ['o4', 'm2', 't1', '-z'], 
    ['o6', 'm2', 't10', '-z'], 
    ['o9', 'm2', 't10', '-z'], 
    ['o5', 'm2', 't15', '-z'], 
    ['o10', 'm2', 't14', '-z'], 
    ['o7', 'm2', 't14', '-z'], 
    ['o8', 'm2', 't3', '-z'], 
    ['o11', 'm2', 't3', '-z'], 
    ['o12', 'm2', 't3', '-z'],
  ], 
  'convergence iteration': 1365
}

```

----

#### AND/OR-Network Based Integer Programming Model for the Flexible Process Planning (FPPCostMinimization.ipynb + FPPTimeMinimization.ipynb)

##### Example

![](https://github.com/Xavier-MaYiMing/Flexible-Process-Planning/blob/main/Example%202.png)

##### The AND/OR-Example

![](https://github.com/Xavier-MaYiMing/Flexible-Process-Planning/blob/main/The%20AND:OR%20network%20of%20Example%202.png)

##### Production cost minimization (FPPCostMinimization.ipynb)

| Sequence  | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Operation | o1   | o2   | o6   | o7   | o8   | o10  | o9   | o11  | o13  | o14  |
| Machine   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m4   |
| Tool      | t1   | t3   | t6   | t7   | t5   | t1   | t1   | t1   | t1   | t11  |
| Direction | +z   | +z   | +z   | +z   | +z   | +z   | +z   | -z   | -z   | +x   |

 - number of variables: 1408
   - binary=1383, integer=25, continuous=0
   
 - number of constraints: 4585
   - linear=4585
   
 - objective value: 735

   

##### Completion time minimization (FPPTimeMinimization.ipynb)

| Sequence  | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Operation | o15  | o16  | o17  | o18  | o19  | o20  | o22  | o23  | o25  | o24  |
| Machine   | m5   | m5   | m5   | m5   | m5   | m5   | m5   | m5   | m5   | m5   |
| Tool      | t9   | t9   | t9   | t6   | t7   | t10  | t10  | t8   | t12  | t12  |
| Direction | -z   | -z   | -z   | -z   | -z   | -y   | +z   | +z   | +z   | +z   |

- number of variables: 3808
   - binary=3758, integer=25, continuous=25
- number of constraints: 6951
   - linear=6951
- objective value: 461.6

---------

#### 0-1 Mathmatical Model for the Flexible Process Planning (FPPCostMinimization_01.ipynb + FPPTimeMinimization_01.ipynb)

##### Example

![](https://github.com/Xavier-MaYiMing/Flexible-Process-Planning/blob/main/Example%201.png)

##### Production cost minimization (FPPCostMinimization_01.ipynb)

| Sequence  | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Operation | o3a  | o13a | o2a  | o1a  | o4   | o9   | o6   | o7   | o10  | o8   | o11  | o12  | o5   |
| Machine   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   | m2   |
| Tool      | t4   | t1   | t1   | t1   | t1   | t10  | t10  | t14  | t14  | t4   | t4   | t4   | t15  |
| Direction | +y   | +z   | +z   | +z   | -z   | -z   | -z   | -z   | -z   | -z   | -z   | -z   | -z   |

- number of variables: 1122
   - binary=1122, integer=0, continuous=0
- number of constraints: 3707
   - linear=3707
- objective value: 833



##### Completion time minimization (FPPTimeMinimization_01.ipynb)

| Sequence  | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Operation | o1   | o2   | o4   | o3   | o6   | o5   | o9   | o14  | o10  | o11  | o12  | o13  | o7   | o8   |
| Machine   | m4   | m4   | m4   | m4   | m4   | m4   | m4   | m4   | m4   | m5   | m4   | m4   | m4   | m4   |
| Tool      | t6   | t6   | t6   | t6   | t6   | t6   | t2   | t2   | t9   | t10  | t1   | t5   | t7   | t7   |
| Direction | -x   | -x   | -x   | -x   | -x   | -x   | +z   | +z   | +z   | -z   | +y   | +y   | +x   | +x   |

- number of variables: 1862

- binary=1862, integer=0, continuous=0

- number of constraints: 3206
   - linear=3206
- objective value: 1062.250
