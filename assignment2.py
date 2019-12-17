import numpy as np
from intcode import readIntCode, runProgram

filepath = 'data2.txt'


input = readIntCode(filepath)
input[1] = 12
input[2] = 2

print("assignment 1:", runProgram(input.copy())[0])

for noun in range(0, 99):
    for verb in range(0, 99):
        adjustedInput = input.copy()
        adjustedInput[1] = noun
        adjustedInput[2] = verb
        result = runProgram(adjustedInput)[0]
        if result == 19690720:
            print('Assignment 2: ', 100 * noun + verb)
            break
