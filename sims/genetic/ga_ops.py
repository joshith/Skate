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


#TODO: FIXME: lot of hacky code here to fix deap ind generator issue with strat dict


def selectOneMax(individual, res_dict):
    log.debug (" individual: %s"%(individual))
    
    fitnessVal = eval_strategy.eval_strategy_with_config(individual)
    
    log.debug ("fitnessVal: %d"%fitnessVal)
    
    res_dict["res"] = fitnessVal,
#     return fitnessVal,


def createOffSpringStrategy(indA, indB):
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

def createOffSpringTradecfg(indA, indB):
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

def createOffSpring(indA, indB):

    indA["strategy_cfg"], indB["strategy_cfg"] = createOffSpringTradecfg(indA["strategy_cfg"], indB["strategy_cfg"])
    indA["trading_cfg"], indB["trading_cfg"] = createOffSpringTradecfg(indA["trading_cfg"], indB["trading_cfg"])

    return indA, indB
    
def createMutantStrategy(indS, indpb):
    
    conf = eval_strategy.get_strategy_vars()
    log.debug ("original: %s"%(indS))
    for key in indS.iterkeys():
        rand = random.random()
        if rand < indpb:
            indS [key] = genParamVal(conf, key)
#             raise Exception("rand: %f %s"%(rand, ind))
    individual = indS
    log.debug ("mutant: %s"%(indS))    
    return individual,  

def createMutantTradecfg(indT, indpb):
    conf = TradingConfig
        
    log.debug ("original: %s"%(indT))
    for key in indT.iterkeys():
        rand = random.random()
        if rand < indpb:
            indT [key] = genParamVal(conf, key)
#             raise Exception("rand: %f %s"%(rand, ind))

    if (indT["stop_loss_enabled"] == False):
        indT["stop_loss_smart_rate"] = False
        indT["stop_loss_rate"] = 0
        
    if (indT["take_profit_enabled"] == False):
        indT["take_profit_rate"] = 0

    individual = indT
    log.debug ("mutant: %s"%(indT))    
    return individual,  

def createMutant (individual, indpb):
    
    individual["strategy_cfg"] = createMutantStrategy(individual["strategy_cfg"])
    individual["trading_cfg"] = createMutantTradecfg(individual["trading_cfg"])
    
    return individual

def configGenerator ():
    return {"strategy_cfg": strategyGenerator(), "trading_cfg": tradingcfgGenerator()}

TradingConfig = {
        'stop_loss_enabled' : {'default': True, 'var': {'type': bool}},
        'stop_loss_smart_rate' : {'default': True, 'var': {'type': bool}},
        'stop_loss_rate' : {'default': 5, 'var': {'type': int, 'min': 1, 'max': 10, 'step': 1 }},
        'take_profit_enabled' : {'default': True, 'var': {'type': bool}},
        'take_profit_rate' : {'default': 10, 'var': {'type': int, 'min': 2, 'max': 20, 'step': 1 }}
        }
def tradingcfgGenerator ():
    cfg_gen = {}
    
    print "tC %s"%(TradingConfig)
    for param_key in TradingConfig.iterkeys():
        cfg_gen [param_key] = genParamVal(TradingConfig, param_key)

    if (cfg_gen["stop_loss_enabled"] == False):
        cfg_gen["stop_loss_smart_rate"] = False
        cfg_gen["stop_loss_rate"] = 0
        
    if (cfg_gen["take_profit_enabled"] == False):
        cfg_gen["take_profit_rate"] = 0
                
    log.debug ("strat: %s"%(cfg_gen))

    return cfg_gen

def strategyGenerator ():
    #strat_confg = { 'period' : {'default': 50, 'var': {'type': int, 'min': 20, 'max': 100, 'step': 1 }},}
    
    # TODO: TBD: NOTE: enhance initial pop generation logic. Right now pure random, We can use heuristics for better pop
    
    conf = eval_strategy.get_strategy_vars()
    strat_gen = {}
    
    for param_key in conf.iterkeys():
        strat_gen [param_key] = genParamVal(conf, param_key)
#         yield param_key, val    
#         yield val
    log.debug ("strat: %s"%(strat_gen))
    return strat_gen

def genParamVal (conf, param_key):
        
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
    elif tp == bool:
        val = random.choice([False, True])
    elif tp == str:
        raise Exception("Unsupported var type str")
    else:
        raise Exception( "Unsupported var type (%s)"%(repr(tp))) 
    
    return val

if __name__ == "__main__":
    import strategy.strategies.ema_rsi as ema_rsi
    
    eval_strategy.g_strategy_class = ema_rsi.EMA_RSI
    
    print ("conf: %s"%(eval_strategy.get_strategy_vars()))
    
    indA = configGenerator ()
    indB = configGenerator ()
    
    print ("\n\nindA: %s \n\n indB:%s "%(indA, indB))
    offA, offB = createOffSpring (indA, indB)
    
    res_dict = dict()
    m = selectOneMax (indA, res_dict)
    print ("indA: %s \n indB: %s \n offA: %s \n offB: %s val: %s"%(indA, indB, offA, offB, m))
    
#EOF