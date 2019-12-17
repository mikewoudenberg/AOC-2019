import numpy as np
from intcode import evalProgram, readIntCode
from util import getBoundingRect
import curses
import time

filepath = 'data15.txt'


class Cell:
    def __init__(self, coord, content, addedBy):
        self.coord = coord
        self.content = content
        self.addedBy = addedBy


input = readIntCode(filepath)


def getMovement(cell1, cell2):
    if cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 1:
        return 3 if cell1[1] - cell2[1] > 0 else 4
    elif cell1[1] == cell2[1] and abs(cell1[0] - cell2[0]) == 1:
        return 2 if cell1[0] - cell2[0] > 0 else 1


def getDirections(currentPos, visited):
    return [(currentPos[0] + x, currentPos[1])
            for x in range(-1, 2, 2) if (currentPos[0] + x, currentPos[1]) not in visited] \
        + [(currentPos[0], currentPos[1] + x) for x in range(-1, 2, 2)
            if (currentPos[0], currentPos[1] + x) not in visited]


def moveRobot(input):
    state = {(0, 0): Cell((0, 0), '.', (0, 0))}
    visited = set()
    currentPos = (0, 0)
    oxygenPos = None
    prevPos = (0, 0)
    backTracking = False
    visited.add(currentPos)
    toVisit = getDirections(currentPos, visited)

    def outp(x):
        nonlocal currentPos
        nonlocal backTracking
        nonlocal oxygenPos
        nonlocal toVisit
        visited.add(currentPos)
        if backTracking:
            if x == 0:
                print('Hit a wall while backtracking')
            elif x == 2:
                print('Found oxygen while backtracking at', currentPos)
        else:
            if x == 0:
                state[currentPos] = Cell(currentPos, '#', prevPos)
                toVisit.pop()
                currentPos = prevPos
            elif x == 1:
                state[currentPos] = Cell(currentPos, '.', prevPos)
                toVisit.pop()
                toVisit += getDirections(currentPos, visited)
            elif x == 2:
                state[currentPos] = Cell(currentPos, 'o', prevPos)
                oxygenPos = currentPos
                print('Found oxygen at', currentPos)

    def inp():
        nonlocal backTracking
        nonlocal currentPos
        nonlocal prevPos
        while toVisit:
            if currentPos == toVisit[-1]:
                toVisit.pop()
            toCell = toVisit[-1]
            movement = getMovement(currentPos, toCell)
            if movement:
                backTracking = False
                prevPos = currentPos
                currentPos = toCell
                return movement

            if backTracking:
                toCell = state[currentPos].addedBy
                movement = getMovement(currentPos, toCell)
                prevPos = currentPos
                currentPos = toCell
                return movement
            else:
                backTracking = True
                toCell = state[currentPos].addedBy
                movement = getMovement(currentPos, toCell)
                prevPos = currentPos
                currentPos = toCell
                return movement

            yield ()
    next(evalProgram(input, inp, outp))
    return (state, oxygenPos)


(grid, oxygen) = moveRobot(input.copy())

steps = 0
current = grid[oxygen]
while True:
    prev = grid[current.addedBy]
    if prev.coord == (0, 0):
        print('Assignment 1:', steps + 1)
        break
    steps += 1
    current = prev


def getExpand(grid, currentPos):
    return [(currentPos[0] + x, currentPos[1])
            for x in range(-1, 2, 2) if grid[(currentPos[0] + x, currentPos[1])].content == '.'] \
        + [(currentPos[0], currentPos[1] + x) for x in range(-1, 2, 2)
            if grid[(currentPos[0], currentPos[1] + x)].content == '.']


stdscr = curses.initscr()


def draw(state):
    x1, x2, y1, y2 = getBoundingRect(list(state.keys()))

    for y in range(y1, y2):

        line = "".join([state.get((x, y), Cell(None, '#', None)).content
                        for x in range(x1, x2)])
        stdscr.addstr(y - y1, 0, line)
    stdscr.refresh()
    time.sleep(0.01)


def fillWithOxygen(grid, start):
    expandTo = getExpand(grid, start)
    minutes = 0
    while expandTo:
        draw(grid)
        nextExpandTo = []
        for coord in expandTo:
            if grid[coord].content == 'o':
                continue
            grid[coord].content = 'o'
            nextExpandTo.extend(getExpand(grid, coord))
        expandTo = nextExpandTo
        minutes += 1
    print('Assignment 2:', minutes)


fillWithOxygen(grid.copy(), oxygen)
