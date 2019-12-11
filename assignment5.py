import numpy as np
from intcode import runProgram

filepath = 'data5.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


input = {i: int(x) for i, x in enumerate(readlines(filepath)[0].split(','))}

stdin = [1]
(_, stdout) = runProgram(input.copy(), stdin)
print("assignment 1:", stdout[-1])

stdin = [5]
(_, stdout) = runProgram(input.copy(), stdin)
print('assignment 2:', stdout[-1])
