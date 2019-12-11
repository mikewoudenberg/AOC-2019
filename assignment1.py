import numpy as np
from functools import reduce

filepath = 'data1.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


modules = readlines(filepath)
fuel = [np.floor(int(x) / 3)-2 for x in modules]
sum = np.sum(fuel)
print('Assignment 1:', sum)

while (any(fuel)):
    fuel = [max(np.floor(int(x) / 3)-2, 0) for x in fuel]
    sum += np.sum(fuel)

print('Assigment 2:', sum)
