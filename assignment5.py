import numpy as np
from intcode import readIntCode, runProgram

filepath = 'data5.txt'
input = readIntCode(filepath)

stdin = [1]
(_, stdout) = runProgram(input.copy(), stdin)
print("assignment 1:", stdout[-1])

stdin = [5]
(_, stdout) = runProgram(input.copy(), stdin)
print('assignment 2:', stdout[-1])
