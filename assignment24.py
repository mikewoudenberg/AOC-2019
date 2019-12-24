from functools import lru_cache
data = """##.#.
##.#.
##.##
.####
.#...
"""


def buildGrid(data):
    grid = [0] * 49
    data = data.replace('#', '1').replace('.', '0')
    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            grid[toCoord(x, y)] = int(char)
    return grid


@lru_cache(maxsize=49)
def toCoord(x, y):
    return (y + 1) * 7 + x + 1


grid = buildGrid(data)


def getNeighbours(x, y, grid):
    return [grid[toCoord(x+1, y)], grid[toCoord(x-1, y)],
            grid[toCoord(x, y + 1)], grid[toCoord(x, y-1)]]


def doStep(grid):
    newGrid = grid.copy()
    for y in range(5):
        for x in range(5):
            cell = grid[toCoord(x, y)]
            neighbours = sum(getNeighbours(x, y, grid))
            if cell and neighbours != 1:
                newGrid[toCoord(x, y)] = 0
                continue
            if (neighbours == 1 or neighbours == 2):
                newGrid[toCoord(x, y)] = 1

    return newGrid


def getBioDiveristy(grid):
    result = []
    for y in range(5):
        for x in range(5):
            result.append(grid[toCoord(x, y)])
    return int(''.join(map(str, result[::-1])), 2)


grids = set()
grids.add(tuple(grid))
while True:
    newGrid = doStep(grid)
    gridTuple = tuple(newGrid)
    if gridTuple in grids:
        print('Assignment 1: ', getBioDiveristy(newGrid))
        break
    grids.add(gridTuple)
    grid = newGrid
