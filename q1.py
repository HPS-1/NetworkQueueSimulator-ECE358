#import random generating library
from numpy import random

counter = 0
list = []

while counter < 1000:
    counter += 1
    list.append(random.exponential(1/75))

counter = 0
mean = 0.0
while counter < 1000:
    mean += list[counter]
    counter += 1
mean = mean/1000
print('mean is:')
print(mean)

counter = 0
variance = 0.0
while counter < 1000:
    variance += (list[counter] - mean) ** 2
    counter += 1
variance = variance/999
print('variance is:')
print(variance)