import utils
import random
import copy

# Author : Charles Coster
# Date of Creation: 07-2019
# Description: Genetic Algorithm Basic Class for the traffic light planning
# Version: 1.0

class Solution : 
    #main class: 1 individual = 1 solution
    #ADD HERE: more parameters for solution
    #group of compat light used initially
    group = []
    #matrix of green fire per time stamp
    TS = []
    #time stamp of a change of group of fire
    _changing_TS = []
    #fitness value of the individual
    fitness = 0

    #Used only when creating the initial population 
    def __init__ (self, ini_g):
        #CC-- TODO: should add here new constraint : max lit time, max/min number of lit, time between litting again
        self.gsize = len(ini_g)
        self.TS = []
        self.group = []
        self._changing_TS = []
        for g in ini_g : 
            self.group.append(utils.Cloning(g))
        indexlist = utils.shuffle_array(self.gsize) + utils.shuffle_array(self.gsize)
        offset = 0 
        #done such that every group in the initial set is used at least once
        while len(self.TS) < 120 :
            if len(self._changing_TS)-offset-1 > len(indexlist) :
                offset += self.gsize 
                indexlist = utils.shuffle_array(self.gsize-1)
            index = indexlist[len(self._changing_TS)-1-offset]
            self._changing_TS.append(len(self.TS))
            if len(self.TS) < (120-19) : 
                #apply a certain group for a random time between min green and 120/numberOfGroup
                randt = random.randint(7, max(round(120/(self.gsize-1)),8))
                while randt > 0 : 
                    self.TS.append(copy.deepcopy(self.group[index]))
                    randt = randt - 1 
            else : 
                t = 120 - len(self.TS)
                while t > 0 : 
                    self.TS.append(copy.deepcopy(self.group[index]))
                    t = t - 1 
        #adapt the fire plan for the intergreen time
        adapt_green_time_interval(self)



    def _const_check (self): 
        #CC-- AD HERE: constraint that need to be enforced (if they do not take too long otherwise when created)
        #ADD for example minimum green time per cycle - maxmimum green time (count number of occurence)
        count = [] 
        OK = False
        for g in self.TS: 
            for fire  in g :  
                if fire not in count : 
                    count.append(fire)
        #check if every light is lit at least once in the cycle 
        if len(count) == 11 : 
            OK = True 
        #it takes too long to check for each every time --> need solution
        # for gf in self.TS : 
        #     for f1 in gf : 
        #         if OK is False : 
        #             break
        #         for f2 in gf : 
        #             if int(f2) in Antag_fire[int(f1)-1] : 
        #                 OK = False
        return OK
        
    #evaluate individual's fitness --> metrics for evolution
    def eval_fitness (self):
        #CC -- for now only metrics is flow per hour --> flow per sec*30
        #CC -- TODO: define here new metrics or improve this one
        fit = 0 
        if self._const_check() is True:
            for g in self.TS : 
                for f in g:
                    #mult used if you want to improve or diminish the impact of certain fire
                    mult = 1  
                    if f == str(10) or f == str(5):
                        mult = 1                 
                    fit = fit +  mult*flow[int(f)]/3600 
        self.fitness = fit * 30
        return fit * 30

#dic of flow per vehicle track associated by light id
flow = {1 : 55, 2 : 410, 3 : 95, 4 : 200, 5 : 400, 6 : 200, 7 : 165, 8 : 360 , 9 : 130 , 10 : 310, 11: 100}

maxflow = 0 
#intergreen time matrix
V_time = []
#antagonist light -- cannot be lit at the same time
Antag_fire = []
#compatible light  -- the opposite
compat_fire = []

#should only be used once when first using this program
def create_possible_group_file(): 
    pg = enum_possible_group(compat_fire)
    fi = open("compatible_group.txt", "w+")
    sortedappended = []

    for group in pg : 
        group.sort()
        toprint = True 
        for i in group : 
            if group.count(i) > 1 : 
                toprint = False 
        if toprint is True and group not in sortedappended: 
            fi.write(str(group) + "\n")
            sortedappended.append(utils.Cloning(group))
        
    fi.close()

#used at init to prepare the relevant list
def create_tables (): 

    for i in range(11):
        V_time.append({})
        Antag_fire.append([])
        compat_fire.append([])

    maxflow = 0

    for el in flow: 
        maxflow += flow[el]
    print("maxflow per hour is:", maxflow)

    file = open("imposs.txt", "r")

    for line in file :
        splitted = line.split('-')
        Vid = int(splitted[0])-1
        Aid = int(splitted[1])-1
        Time = int(splitted[2])
        V_time[Vid][Aid] = Time 
        Antag_fire[Vid].append(Aid+1)

    for l in range(11) : 
        for i in range(1,12):
            if i not in Antag_fire[l] : 
                compat_fire[l].append(i)

    file.close()

    return [flow, maxflow, Antag_fire, compat_fire, V_time ]
 
#return a list of compatible group of light to create the an init solution
def create_init_sol (Possible_group):
    groupl = []
    sol_ok = False
    while sol_ok is False :
        rand = random.randint(0,len(Possible_group)-1)
        if Possible_group[rand] not in groupl : 
            groupl.append(utils.Cloning(Possible_group[rand]))
        count = [] 
        for g in groupl: 
            for fire  in g :  
                if fire not in count : 
                    count.append(fire)
        # to have every light lit during a cycle
        if len(count) == 11 : 
            sol_ok = True

    return groupl

#enumerate all the possibility of compatible group of fire                
def enum_possible_group (compat_fire): 
    possible_group  = []
    #for each light create the list of compat by taking the intersection of compatibality matrix
    for i in range(1,12): 
        group = []
        group.append(i)
        for j in compat_fire[i-1] :  
            group.append(j)
            if group not in possible_group and group.count(j) < 2: 
                possible_group.append(utils.Cloning(group))
            for k in utils.intersection(compat_fire[i-1],compat_fire[j-1]) : 
                group.append(k)
                if group.sort() not in possible_group  and group.count(j) < 2: 
                    possible_group.append(utils.Cloning(group))
                for l in utils.intersection(utils.intersection(compat_fire[i-1],compat_fire[j-1]),compat_fire[k-1]):
                    group.append(l)
                    if group.sort() not in possible_group and group.count(j) < 2 : 
                        possible_group.append(utils.Cloning(group))
                    group.remove(l)
                group.remove(k)
            group.remove(j)
    return possible_group

#select the new generation and reproduce them
def offspring_selection (solset, centaines):
    #proportionate selection for now on p of reproduction = fitness/total
    #CC -- TODO: can and should be change - try rank based selection or tournament selection
    offsprings = []
    total = 0 
    for sol in solset : 
        total += sol.fitness 
    for sol in solset :
        for i in range(round(centaines*100*sol.fitness/total)) : 
            offsprings.append(copy.deepcopy(sol))
    return offsprings
    
              
# change for a solution the TS so that intergreen time are respected -- called on init and mutation
def adapt_green_time_interval(sol): 
    #CC -- TODO: this does not yet take into account the transition between 120s and 0s
    #CC -- TODO: this still reduce sometime the green time of a fire < min green (7s)
    for change in sol._changing_TS :
        if change == 0 : 
            continue 
        t1 = change - 1 
        t2 = change 
        gtime = 0
        for f1 in sol.TS[t1]:
            for f2 in sol.TS[t2]: 
                if int(f2) in V_time[int(f1)-1]  : 
                    gtime = V_time[int(f1)-1][int(f2)]
                    dect1 = 0
                    dect2 = 0
                while gtime > 0 : 
                    #supress green time on both side when pair or on upperside when not
                    #CC -- TODO: adapt on the more intelligent side --> should not go under 7s
                    if gtime % 2 == 0 : 
                        if f1 in sol.TS[t1-dect1] : 
                            sol.TS[t1-dect1].remove(f1)
                        if f2 in sol.TS[t2-dect2] and (t2+dect2) <120: #if t2+dect2 >120 on decremente trop gtime mais pg pour le moment
                            sol.TS[t2+dect2].remove(f2)
                        dect1 = dect1+1
                        dect2 = dect2+1
                        gtime = gtime - 2
                    else : 
                        sol.TS[t2+dect2].remove(f2)
                        gtime = gtime - 1 
                        dect2 = dect2+1

# return best individual between precedent best and whole new set                       
def update_best(prec, newset) : 
    bfit = prec.eval_fitness()
    Best = prec
    for sol in newset : 
        if sol.fitness > bfit : 
                bfit = sol.fitness
                Best = sol
    return Best

# mutate the TS of an individual depending on proba --> Safe modification only ! 
def mutation(sol, probaput, probaremove): 
    #CC -- mutation list: add a green fire for a certain timespan, remove a certain green fire for a certain timespan
    #CC -- TODO: Find new possible mutation (very few here)
    #CC -- TODO: Should add here new constraint also 
    #to be chosen --> want to add group or want to add or remove specific light 
    p1 = random.randint(0,100)
    p2 = random.randint(0,100)
    #bool to see if mutation does not corrupt integrity of the solution
    problem = False 
    if p1 < probaput : 
        fire = str(random.randint(1,11))
        r = random.randint(1,len(sol._changing_TS)-2)
        ts = sol._changing_TS[r]
        ts_length = sol._changing_TS[r+1]-sol._changing_TS[r]
        for i in range(ts_length) :
            if problem is True : 
                break
            for f in sol.TS[ts+i] : 
                if int(fire) in Antag_fire[int(f) - 1] : 
                    problem = True
        if problem is False: 
            for i in range(ts_length) :
                if fire not in sol.TS[ts+i] : 
                    sol.TS[ts+i].append(fire)
    if p2 < probaremove :
        r = random.randint(1,len(sol._changing_TS)-2)
        ts = sol._changing_TS[r]
        ts_length = sol._changing_TS[r+1]-sol._changing_TS[r]
        r2 = random.randint(0, ts_length-1)
        if len(sol.TS[ts+r2]) > 1 :
            r3 = random.randint(1, len(sol.TS[ts+r2]))
            fire = sol.TS[ts+r2][r3-1]
            for i in range(ts_length): 
                if fire in sol.TS[ts+i]: 
                    sol.TS[ts+i].remove(fire)

    adapt_green_time_interval(sol)

