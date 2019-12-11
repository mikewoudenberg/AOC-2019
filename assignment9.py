import numpy as np
from intcode import runProgram

filepath = 'data9.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


input = {i: int(x) for i, x in enumerate(readlines(filepath)[0].split(','))}

stdout = []
(_, stdout) = runProgram(input.copy(), [1])
print('Assignment 1: ', stdout[0])

(_, stdout) = runProgram(input.copy(), [2])
print('Assignment 2: ', stdout[0])
