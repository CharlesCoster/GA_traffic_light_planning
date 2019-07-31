import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors
import random   
import Solution  
import utils

# Author : Charles Coster
# Date of Creation: 07-2019
# Description: Genetic Algorithm main loop for the traffic light planning
# Version: 1.0

#Main step of a GA: Initialization - Begin Loop: Evaluation -> Selection -> Reproduction -> Mutation :End Loop

mingreen = 7 #seconds
initial_set = []
[flow, maxflow, antag_fire, compat_fire, v_time ] = Solution.create_tables()

possible_group = utils.import_possible_g("compatible_group.txt")

sol_init = Solution.create_init_sol(possible_group)
Best = Solution.Solution(sol_init)

#creation of the initial solution set - size = 10 -- increase for more initial diversity
while len(initial_set) < 50 : 
    sol_init = Solution.create_init_sol(possible_group)
    initial = Solution.Solution(sol_init)
    if initial.eval_fitness() > 0  : 
        initial_set.append(initial)

Best = Solution.update_best(Best, initial_set)

[mean, stdvalue] = utils.get_stats(initial_set)
print("mean fitness :", mean,", std :", stdvalue, ", best:", Best.fitness)
    
offp_set = Solution.offspring_selection(initial_set, 1)

#Main evolution loop - generation = 150 
#CC -- TODO : keep a list of the best solution found for all the iteration or change in fitness
for i in range (150): 
    Best = Solution.update_best(Best, offp_set)

    [mean, stdvalue] = utils.get_stats(offp_set)
    print("epoch :" ,i, ", mean fitness :", mean,", std :", stdvalue,", best:", Best.fitness, )

    for solution in offp_set:
        Solution.mutation(solution, 50, 20)

    Best = Solution.update_best(Best, offp_set)

    [mean, stdvalue] = utils.get_stats(offp_set)
    print("epoch :" ,i, ", mean fitness :", mean,", std :", stdvalue, ", best:", Best.fitness)

    offp_set = Solution.offspring_selection(offp_set, 3)

#plot best of all solution
utils.plot_solution(Best)
