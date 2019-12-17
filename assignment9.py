import numpy as np
from intcode import readIntCode, runProgram

filepath = 'data9.txt'

input = readIntCode(filepath)

stdout = []
(_, stdout) = runProgram(input.copy(), [1])
print('Assignment 1: ', stdout[0])

(_, stdout) = runProgram(input.copy(), [2])
print('Assignment 2: ', stdout[0])
