import numpy as np
def uniform_var(max):
    return np.random.uniform(0,max,None)
def normal_var(loc,scale):
    return np.random.normal(loc,scale,None)
def exponential_var(scale = 1.0):
    return  np.random.exponential(scale,None)
def gamma_var(shape = 1.0,scale = 1.0):
    return np.random.gamma(shape,scale,None)
def weibull(shape = 1):
    return np.random.weibull(shape,None)
def laplace_var(loc,scale = 1.0):
    return np.random.laplace(loc,scale,None)
def rayleigh_var(scale = 1.0):
    return np.random.rayleigh(scale,None)
def beta_var(a,b):
    return np.random.beta(a,b,None)