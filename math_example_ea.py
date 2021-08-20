import os
import sys
import time
import math

import numpy as np
# import tensorflow as tf

from EA_Util import EA_Util

UNIT = 60.0/65532
LINT = -30.0

def eval_func(individual):
    x1 = 0
    for i in range(16):
        x1 = x1 * 2 + individual[i]
    x1 = LINT + x1 * UNIT
    x2 = 0
    for i in range(16, 32):
        x2 = x2 * 2 + individual[i]
    x2 = LINT + x2 * UNIT
    return 100 + x1 * math.sin(x1) + x2 * math.sin(x2)

ea_helper = EA_Util(
    name='EA_Exp',
    pop_size=20,
    gen_size=32,
    eval_fun=eval_func,
    max_gen=100
)
elite = ea_helper.evolution()
print(ea_helper.fitness[elite]-100)
print('Hello')
print('Bye')