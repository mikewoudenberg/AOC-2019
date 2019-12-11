import numpy as np
from intcode import evalProgram

filepath = 'data11.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


input = {i: int(x) for i, x in enumerate(readlines(filepath)[0].split(','))}


def moveRobot(input, startColor):
    state = {(0, 0): startColor}
    currentPos = (0, 0)
    direction = 0
    turnMode = False
    painted = set()

    def outp(x):
        nonlocal turnMode
        nonlocal direction
        nonlocal currentPos
        if turnMode:
            direction = (direction + (2*x-1) + 4) % 4
            if direction == 0:
                currentPos = (currentPos[0], currentPos[1] - 1)
            elif direction == 1:
                currentPos = (currentPos[0]+1, currentPos[1])
            elif direction == 2:
                currentPos = (currentPos[0], currentPos[1] + 1)
            elif direction == 3:
                currentPos = (currentPos[0]-1, currentPos[1])
        else:
            state[currentPos] = x
            painted.add(currentPos)

        turnMode = not turnMode

    def inp():
        while True:
            return state.get(currentPos, 0)
            yield ()
    for i in evalProgram(input, inp, outp):
        pass
    return state


print('Assignment 1:', len(moveRobot(input.copy(), 0)))
pixels = moveRobot(input.copy(), 1)
print('Assignment 2', pixels)
