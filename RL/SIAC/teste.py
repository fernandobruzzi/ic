import random
from scipy.stats import dirichlet

probs = dirichlet((1,1)).rvs(2)
print(probs, probs[0])
a, b = probs[0]
print(a, b)