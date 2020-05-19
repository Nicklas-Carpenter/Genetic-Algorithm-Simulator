import numpy as np 
import matplotlib.pyplot as plt 
from random import random, randint

n = 10

def mk_cos(w):
    return lambda t : np.cos(w * t)

X = []
for k in range(n):
    X.append(mk_cos(np.pi / (n - k)))


t = np.linspace(0, n * np.pi, num = 100 * n)

x = np.zeros((len(t),))
for i in range(1,n):
    a = randint(0, 1) * (2 *random() - 1)
    x += a * X[i](t)
    print("X[{0}]: {1}".format(i, a))

y = np.cos(np.pi * t)
plt.plot(t, y, "g:", t, x, "r")

plt.show()