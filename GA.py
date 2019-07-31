import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors
import random   
import Solution  
import utils

mingreen = 7 #seconds

[flow, maxflow, antag_fire, compat_fire, v_time ] = Solution.create_tables()

possible_group = utils.import_possible_g("compatible_group.txt")

initial_set = []
sol_init = Solution.create_init_sol(possible_group)
Best = Solution.Solution(sol_init)

while len(initial_set) < 10 : 
    sol_init = Solution.create_init_sol(possible_group)
    initial = Solution.Solution(sol_init)
    if initial.eval_fitness() > 0  : 
        initial_set.append(initial)

Best = Solution.update_best(Best, initial_set)


[mean, stdvalue] = utils.get_stats(initial_set)
print("mean fitness :", mean,", std :", stdvalue, ", best:", Best.fitness)
    
offp_set = Solution.offspring_selection(initial_set)

for i in range (200): 
    Best = Solution.update_best(Best, offp_set)

    [mean, stdvalue] = utils.get_stats(offp_set)
    print("epoch :" ,i, ", mean fitness :", mean,", std :", stdvalue,", best:", Best.fitness, )

    for solution in offp_set:
        Solution.mutation(solution, 50, 20)

    Best = Solution.update_best(Best, offp_set)

    [mean, stdvalue] = utils.get_stats(offp_set)
    print("epoch :" ,i, ", mean fitness :", mean,", std :", stdvalue, ", best:", Best.fitness)

    offp_set = Solution.offspring_selection(offp_set)


utils.plot_solution(Best)
