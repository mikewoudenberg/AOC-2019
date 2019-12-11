import numpy as np
from intcode import runProgram

filepath = 'data2.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


input = {i: int(x) for i, x in enumerate(readlines(filepath)[0].split(','))}
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
