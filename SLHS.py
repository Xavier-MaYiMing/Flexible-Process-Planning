#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/8 15:51
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : SLHS.py
# @Statement : The Sequence Learning Harmony Search (SLHS) for the Flexible Process Planning (FPP) problem
# @Reference : Luo K. A sequence learning harmony search algorithm for the flexible process planning problem[J]. International Journal of Production Research, 2022, 60(10): 3182-3200.
import copy
import random
import matplotlib.pyplot as plt


def obj(sol, specs, MUC, TUC, MCC, TCC, SCC):
    """
    Calculate the objective values of a solution
    :param sol: the solution
    :param specs: specifications
    :param MUC: Machine Usage Cost
    :param TUC: Tool Usage Cost
    :param MCC: Machine Changeover Cost
    :param TCC: Tool Changeover Cost
    :param SCC: Setup Changeover Cost
    :return:
    """
    if not check_feasibility(sol, specs):
        return 1e6
    machine = sol[0][1]
    tool = sol[0][2]
    setup = sol[0][3]
    AMUC = MUC[machine]  # accumulated machine usage cost
    ATUC = TUC[tool]  # accumulated tool usage cost
    AMCC = 0  # accumulated machine changeover cost
    ATCC = 0  # accumulated tool changeover cost
    ASCC = 0  # accumulated setup changeover cost
    for i in range(1, len(sol)):
        if machine != sol[i][1]:
            AMCC += MCC
        if machine != sol[i][1] or tool != sol[i][2]:
            ATCC += TCC
        if machine != sol[i][1] or setup != sol[i][3]:
            ASCC += SCC
        machine = sol[i][1]
        tool = sol[i][2]
        setup = sol[i][3]
        AMUC += MUC[machine]
        ATUC += TUC[tool]
    return AMUC + ATUC + AMCC + ATCC + ASCC


def check_feasibility(sol, specs):
    """
    Check the feasibility of the solution
    :param sol: the solution
    :param specs: specifications
    :return:
    """
    temp_sol = [item[0] for item in sol]
    for key in specs.keys():
        if key in temp_sol:
            for item in specs[key].prior:
                if item in temp_sol and temp_sol.index(key) < temp_sol.index(item):
                    return False
    return True


def cal_precedence(P):
    """
    Calculate the precedence constraint satisfaction status
    :param P: the indicative matrix of precedence satisfaction status
    :return:
    """
    n_pos_ops = len(P)
    u = [1] * n_pos_ops
    for j in range(n_pos_ops):
        for i in range(n_pos_ops):
            if P[i][j] != 0:
                u[j] = 0
                break
    return u


def main(ops, specs, MUC, TUC, MCC, TCC, SCC, hms, ni):
    """
    The main function of the SLHS for the FPP problem
    :param ops: operations
    :param specs: specifications
    :param MUC: Machine Usage Cost
    :param TUC: Tool Usage Cost
    :param MCC: Machine Changeover Cost
    :param TCC: Tool Changeover Cost
    :param SCC: Setup Changeover Cost
    :param hms: harmony memory size
    :param ni: the number of improvisations (iterations)
    :return:
    """
    # Step 1. Initialization
    sols = []  # solutions
    score = []  # the score of solutions
    n_ops = len(ops)  # the number of operations
    n_pos_ops = len(specs)  # the number of all possible operations
    ind2ops = list(specs.keys())  # index -> operations
    ops2ind = {}  # operations -> index
    for i in range(n_pos_ops):
        ops2ind[ind2ops[i]] = i
    P = []  # the indicative matrix of precedence satisfaction status
    for i in specs.keys():
        P.append([])
        i_ind = ops2ind[i]
        for j in specs.keys():
            if i in specs[j].prior:
                P[i_ind].append(1)
            else:
                P[i_ind].append(0)
    u = cal_precedence(P)  # the precedence constraint satisfaction status
    v = [1] * n_pos_ops  # the selectable status
    q = [u[i] * v[i] for i in range(n_pos_ops)]  # the qualification status

    # Step 1.1. Harmony memory initialization
    for _ in range(hms):
        temp_sol = []
        temp_P = copy.deepcopy(P)
        temp_v = v.copy()
        temp_q = q.copy()
        for k in range(n_ops):
            cs = [j for j in range(n_pos_ops) if temp_q[j]]  # the candidate set
            temp_j_ind = random.choice(cs)  # the index of the selected operation
            temp_j = ind2ops[temp_j_ind]  # the selected operation
            temp_m = random.choice(specs[temp_j].machine)  # the selected machine
            temp_t = random.choice(specs[temp_j].tool)  # the selected tool
            temp_d = random.choice(specs[temp_j].direction)  # the selected direction
            temp_v[temp_j_ind] = 0
            temp_P[temp_j_ind] = [0] * n_pos_ops
            if specs[temp_j].alternative:
                for alt in specs[temp_j].alternative:
                    alt_ind = ops2ind[alt]
                    temp_v[alt_ind] = 0
                    temp_P[alt_ind] = [0] * n_pos_ops
            temp_u = cal_precedence(temp_P)
            temp_q = [temp_u[i] * temp_v[i] for i in range(n_pos_ops)]
            temp_sol.append([temp_j, temp_m, temp_t, temp_d])
        sols.append(temp_sol)
        score.append(obj(temp_sol, specs, MUC, TUC, MCC, TCC, SCC))
    gbest = min(score)  # the global best score
    gbest_sol = sols[score.index(gbest)]  # the global best solution
    gworst = max(score)  # the global worst score
    iter_best = []  # the global best score of each iteration
    con_iter = 0  # the convergence iteration

    # Step 2. The main loop
    for t in range(ni):

        # Step 2.1. Generate a new harmony
        co = []  # the current operation
        temp_sol = []
        hmcr = random.normalvariate(n_ops / (1 + n_ops), 1 / (1 + n_ops))  # harmony memory consideration rate
        temp_P = copy.deepcopy(P)
        temp_v = v.copy()
        temp_q = q.copy()

        for k in range(n_ops):  # memory consideration
            cs = [j for j in range(n_pos_ops) if temp_q[j]]  # the candidate set
            tab = 0  # the learning success flag
            if random.random() < hmcr:
                rs = [i for i in range(hms)]  # the sample set
                if k == 0:
                    tab = 1
                    ind = random.choice(rs)
                    temp_sol.append(sols[ind][0].copy())
                else:
                    while rs:
                        ind = random.choice(rs)
                        flag = False
                        for r in range(n_ops - 1):
                            if sols[ind][r][0] == co and ops2ind[sols[ind][r + 1][0]] in cs:
                                rs = []
                                tab = 1
                                temp_sol.append(sols[ind][r + 1].copy())
                                flag = True
                                break
                        if not flag:
                            rs.remove(ind)
                        else:
                            break
            if tab == 0:  # harmony randomization
                temp_j_ind = random.choice(cs)  # the index of the selected operation
                temp_j = ind2ops[temp_j_ind]  # the selected operation
                temp_m = random.choice(specs[temp_j].machine)  # the selected machine
                temp_t = random.choice(specs[temp_j].tool)  # the selected tool
                temp_d = random.choice(specs[temp_j].direction)  # the selected direction
                temp_sol.append([temp_j, temp_m, temp_t, temp_d])
            temp_j = temp_sol[-1][0]
            temp_j_ind = ops2ind[temp_j]
            temp_v[temp_j_ind] = 0
            temp_P[temp_j_ind] = [0] * n_pos_ops
            if specs[temp_j].alternative:
                for alt in specs[temp_j].alternative:
                    alt_ind = ops2ind[alt]
                    temp_v[alt_ind] = 0
                    temp_P[alt_ind] = [0] * n_pos_ops
            co = temp_j  # the current operation
            temp_u = cal_precedence(temp_P)
            temp_q = [temp_u[i] * temp_v[i] for i in range(n_pos_ops)]
        for k in range(1, n_ops):  # pitch adjustment
            temp_operation = temp_sol[k][0]
            if temp_sol[k - 1][1] in specs[temp_operation].machine:
                temp_sol[k][1] = temp_sol[k - 1][1]
            if temp_sol[k - 1][2] in specs[temp_operation].tool:
                temp_sol[k][2] = temp_sol[k - 1][2]
            if temp_sol[k - 1][3] in specs[temp_operation].direction:
                temp_sol[k][3] = temp_sol[k - 1][3]

        # Step 2.2. Is it superior to the worst?
        temp_score = obj(temp_sol, specs, MUC, TUC, MCC, TCC, SCC)
        if temp_score < gworst:
            gworst_ind = score.index(gworst)
            sols[gworst_ind] = temp_sol
            score[gworst_ind] = temp_score
            gworst = max(score)
        if temp_score < gbest:
            gbest = temp_score
            gbest_sol = copy.deepcopy(temp_sol)
            con_iter = t + 1
        iter_best.append(gbest)

    # Step 3. Sort the results
    x = [i for i in range(ni)]
    plt.figure()
    plt.plot(x, iter_best, linewidth=2, color='blue')
    plt.xlabel('Iteration number')
    plt.ylabel('Global optimal value')
    plt.title('Convergence curve')
    # plt.savefig('convergence curve.png')
    plt.show()
    return {'best score': gbest, 'best solution': gbest_sol, 'convergence iteration': con_iter}


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
