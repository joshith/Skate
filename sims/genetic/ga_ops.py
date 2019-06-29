#! /usr/bin/env python
# '''
#  OldMonk Auto trading Bot
#  Desc:  Genetic Optimizer
# Copyright 2019, Joshith Rayaroth Koderi, OldMonk Bot. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import random

import eval_strategy
from utils import getLogger

# __name__ = "EA-OPS"
log = getLogger (__name__)
log.setLevel (log.CRITICAL)

strat_config = eval_strategy.get_strategy().config

#TODO: FIXME: lot of hacky code here to fix deap ind generator issue with strat dict


def selectOneMax(individual, res_dict):
    log.debug (" individual: %s"%(individual))
    
    fitnessVal = eval_strategy.eval_strategy_with_config(individual)
    
    log.debug ("fitnessVal: %d"%fitnessVal)
    
    res_dict["res"] = fitnessVal,
#     return fitnessVal,

def createOffSpring(indA, indB):

    ind1, ind2 = indA,indB
    
    size = len(ind1)
    cxpoint1 = random.randint(1, size)

    keys = random.sample(list(ind1), cxpoint1)
    
    log.debug ("size: %d cxpoint1: %d keys; %s"%(size, cxpoint1, keys))
    
    for key in keys:
        #swap values
        log.debug ("swapping key: %s"%(key))
        tmp = ind1[key]
        ind1[key], ind2[key] = ind2[key], tmp
            
    indA= ind1
    indB= ind2
    return indA, indB
    
def createMutant(individual, indpb):
    
    ind = individual
    
    log.debug ("original: %s"%(ind))
    for key in ind.iterkeys():
        rand = random.random()
        if rand < indpb:
            ind [key] = genParamVal(key)
#             raise Exception("rand: %f %s"%(rand, ind))
    individual = ind
    log.debug ("mutant: %s"%(ind))    
    return individual,  

def strategyGenerator ():
    #strat_confg = { 'period' : {'default': 50, 'var': {'type': int, 'min': 20, 'max': 100, 'step': 1 }},}
    
    # TODO: TBD: NOTE: enhance initial pop generation logic. Right now pure random, We can use heuristics for better pop
    
    conf = strat_config
    strat_gen = {}
    
    for param_key in conf.iterkeys():
        strat_gen [param_key] = genParamVal(param_key)
#         yield param_key, val    
#         yield val
    log.debug ("strat: %s"%(strat_gen))
    return strat_gen

def genParamVal (param_key):
    conf = strat_config
        
    param_conf = conf[param_key]
    var = param_conf['var']
    tp = var['type']
    
    val = 0
    if tp == int:
        r_min = var['min']
        r_max = var['max']
        r_step = var.get('step')
        #get val
        val = random.randrange (r_min, r_max+1, r_step)
    elif tp == float :
        r_min = var['min']
        r_max = var['max']
        r_step = var.get('step')
        val = round(random.uniform (r_min, r_max), 2)
    elif tp == str:
        raise Exception("Unsupported var type str")
    else:
        raise Exception( "Unsupported var type (%s)"%(repr(tp))) 
    
    return val

if __name__ == "__main__":
    
    print ("conf: %s"%(strat_config))
    
    indA = strategyGenerator ()
    indB = strategyGenerator ()
    
    print ("indA: %s \n indB:%s "%(indA, indB))
    offA, offB = createOffSpring (indA, indB)
    
    m = selectOneMax (indA)
    print ("indA: %s \n indB: %s \n offA: %s \n offB: %s val: %s"%(indA, indB, offA, offB, m))
    
#EOF