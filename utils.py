import Solution
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors

def get_stats(sol_set) : 
    value = []
    for sol in sol_set :
        value.append(sol.eval_fitness())
    return [np.mean(value), np.std(value)]


def Cloning(li1): 
    li_copy = li1[:] 
    return li_copy 

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

def shuffle_array(size) : 
    arr = list(range(size))
    random.shuffle(arr)
    return arr

    
def import_possible_g (name): 
    fi = open(name, "r")
    p = []
    for line in fi :
        g = [] 
        sp = line.replace('[','').replace(']','').replace(' ','').replace('\n','').split(",")
        for el in sp : 
            g.append(el)
        p.append(Cloning(g))
    return p 

def plot_solution(sol): 
    plan = np.eye(11,120)
    for i in range(11):
        for j in range(120):
            plan[i][j] = -10

    for i in range(120) : 
        g = sol.TS[i]
        for f in g: 
            plan[int(f)-1][i] = 10

    cmap1 = plt.get_cmap('jet',10)
    cmap1.set_over('green')
    cmap1.set_under('red')

    plt.pcolor(plan, cmap=cmap1, vmax=1, vmin=0,edgecolor = 'k', linewidths=1)

    plt.show()

