import numpy as np
from intcode import evalProgram, readIntCode
from util import getBoundingRect

filepath = 'data11.txt'
input = readIntCode(filepath)


def moveRobot(input, startColor):
    state = {(0, 0): startColor}
    currentPos = (0, 0)
    direction = 0
    turnMode = False

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
        turnMode = not turnMode

    def inp():
        while True:
            return state.get(currentPos, 0)
            yield ()
    next(evalProgram(input, inp, outp))
    return state


print('Assignment 1:', len(moveRobot(input.copy(), 0)))

print('Assignment 2:')
pixels = moveRobot(input.copy(), 1)
x1, x2, y1, y2 = getBoundingRect(
    [key for (key, value) in pixels.items() if value == 1])
for y in range(y1, y2):
    print("".join(['.' if pixels.get((x, y), 0)
                   == 0 else '█' for x in range(x1, x2)]))
