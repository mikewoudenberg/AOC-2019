import math
from itertools import accumulate
inputFile = 'data16.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


inp = list(map(int, readlines(inputFile)[0]))
conv = [0, 1, 0, -1]


def doPhase(digits):
    result = []
    for i in range(len(digits)):
        row = 0
        for j, digit in enumerate(digits):
            repeat = (i+1)
            convIndex = ((j + 1) // repeat) % 4
            row += conv[convIndex] * digit
        result.append(abs(row) % 10)

    return result


data = inp.copy()
for i in range(100):
    data = doPhase(data)

print('Assignment 1:', ''.join(map(str, data[0:8])))

data = [int(x) for x in inp*10000]
offset = int(''.join(map(str, data[:7])))

n = len(data)
rightHalf = data.copy()[n//2-1:]
for i in range(100):
    rightHalf = list(map(lambda x: x % 10, accumulate(
        rightHalf[::-1])))[n//2-1::-1]

offsetInRight = offset - len(rightHalf)
print("Assignment 2:", ''.join(
    map(str, rightHalf[offsetInRight:offsetInRight+8])))
