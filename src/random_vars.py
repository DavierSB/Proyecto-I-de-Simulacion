import numpy as np
import random
from distribution import Distribution
def uniform_var(max = 0.5):
    return np.random.uniform(0,max,None)
def normal_var(loc = 0,scale = 1):
    return np.random.normal(loc, scale,None)
def exponential_var(scale = 1.0):
    return  np.random.exponential(scale,None)
def gamma_var(shape = 1.0,scale = 1.0):
    return np.random.gamma(shape,scale,None)
def weibull(shape = 1):
    return np.random.weibull(shape,None)

def get_n_random_distributions(n):
    distributions = {0 : uniform_var, 1 : normal_var, 2 : exponential_var, 3 : gamma_var, 4 : weibull}
    rnd_dstrbtns = []
    for i in range(0, n):
        rnd_dstrbtns.append(Distribution(distributions[random.randint(0, 4)]))
    return rnd_dstrbtns