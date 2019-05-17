import os
import time
import math
import copy
import random

import numpy as np
import matplotlib.pyplot as plt

class EA_Util:
    def __init__(self, name, pop_size, gen_size, eval_fun=None, max_gen=100, drop_set=[], sp_set=[]):
        self.name = name
        self.pop_size = pop_size
        self.gen_size = gen_size
        self.max_gen = max_gen
        self.drop_set = drop_set
        self.remain_set = []
        self.sp_set = sp_set

        if eval_fun == None:
            raise Exception("Undefined Eval Function")
        else:
            self.eval_fun = eval_fun
        
        for i in range(gen_size):
            if i not in self.drop_set:
                self.remain_set.append(i)
        self.cnt_remain = len(self.remain_set)
        print('Remain', self.cnt_remain)
        self.a = int(math.log(self.cnt_remain, 2)) // 2
        self.b = int(math.log(self.cnt_remain, 2))
        print('mutation interval: [%d, %d]' % (self.a, self.b))

        self._init_pop()
    
    def _init_pop(self):
        population = []
        for _ in range(self.pop_size):
            individual = [1] * self.gen_size
            for x in range(self.gen_size):
                individual[x] = random.randint(0, 1)
            for x in self.drop_set:
                individual[x] = 0
            for x in self.sp_set:
                individual[x] = 1
            population.append(individual)
        self.population = population
        self.fitness = [-1] * self.pop_size
    
    def _mutation(self, individual, cnt=1):
        new_chrom = individual.copy()
        for _ in range(cnt):
            s = random.randint(self.a, self.b)
            t = random.sample(self.remain_set, s)
            for x in t:
                new_chrom[x] = 1 - new_chrom[x]
        for x in self.sp_set:
            new_chrom[x] = 1
        return new_chrom
    
    def _eval_pop(self):
        for x in range(self.pop_size):
            if self.fitness[x] < 0:
                self.fitness[x] = self.eval_fun(self.population[x])
    
    def _reproduct(self, sur_cnt=None):
        temp_fit = np.array(self.fitness)
        if sur_cnt == None:
            sur_cnt = 5
        temp_ind = np.argsort(temp_fit)
        survival = temp_ind[-1*sur_cnt:]
        obsolete = temp_ind[:-1*sur_cnt]
        print('\tsurvival:', survival)
        print('\tobsolete:', obsolete)
        for i in obsolete:
            x = random.choice(survival)
            self.population[i] = self._mutation(self.population[x])
            self.fitness[i] = -1
    
    def evolution(self):
        fit_rec = []
        self._eval_pop()
        print('Init pop')
        fit_rec.append(max(self.fitness))
        best_fit = round(max(self.fitness), 4)
        tmp_fit = self.fitness.copy()
        for i in range(self.pop_size):
            tmp_fit[i] = round(tmp_fit[i], 4)
        print('\tBest Fitness: %.4f' % (best_fit))
        print('\tPop Fitness:', tmp_fit)
        for gen in range(1, self.max_gen+1):
            print('%d Evolution' % (gen))
            self._reproduct()
            self._eval_pop()
            fit_rec.append(max(self.fitness))
            best_fit = round(max(self.fitness), 4)
            tmp_fit = self.fitness.copy()
            for i in range(self.pop_size):
                tmp_fit[i] = round(tmp_fit[i], 4)
            print('\tBest Fitness: %.4f' % (best_fit))
            print('\tPop Fitness:', tmp_fit)
        index = self.fitness.index(max(self.fitness))
        plt.figure()
        plt.plot(range(self.max_gen+1), fit_rec, marker='*')
        plt.grid(True)
        plt.xlabel('Generation(th)')
        plt.ylabel('Current Best Fitness')
        plt.legend()
        plt.savefig('./%s-%d.png' % (self.name, int(time.time())))
        return index