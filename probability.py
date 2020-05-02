import random

def create_uniform_generator(a, b):
    return lambda : random.uniform(a, b)

def create_exponential_generator(lam):
    return lambda : random.expovariate(lam)

def create_gauss_generator(mu, sigma):
    return lambda : random.gauss(mu, sigma)