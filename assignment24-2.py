from collections import Counter, defaultdict

data = """##.#.
##.#.
##.##
.####
.#...
"""


def buildGrid(data):
    grid = defaultdict(int)
    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                grid[(x, y, 0)] = 1
    return grid


def wrapAroundWithLevel(coord, movement):
    res = tuple([coord[0] + movement[0], coord[1] + movement[1], coord[2]])
    if res[0] >= 5:
        res = tuple([3, 2, coord[2] + 1])
    elif res[0] < 0:
        res = tuple([1, 2, coord[2] + 1])
    elif res[1] >= 5:
        res = tuple([2, 3, coord[2] + 1])
    elif res[1] < 0:
        res = tuple([2, 1, coord[2] + 1])
    return res


def getNeighbourhood(coord):
    (x, y, level) = coord
    if (x == 1 or x == 3) and (y == 1 or y == 3):
        return [(x + 1, y, level), (x - 1, y, level),
                (x, y+1, level), (x, y-1, level)]
    if x == 0 or x == 4 or y == 0 or y == 4:
        return [wrapAroundWithLevel(coord, [0, 1]), wrapAroundWithLevel(coord, [0, -1]),
                wrapAroundWithLevel(coord, [1, 0]), wrapAroundWithLevel(coord, [-1, 0])]
    if x == 2 and y == 1:
        return [(x + 1, y, level), (x - 1, y, level),
                (x, y-1, level), (0, 0, level - 1),
                (1, 0, level - 1), (2, 0, level - 1),
                (3, 0, level - 1), (4, 0, level - 1)]
    if x == 2 and y == 3:
        return [(x + 1, y, level), (x - 1, y, level),
                (x, y+1, level), (0, 4, level - 1),
                (1, 4, level - 1), (2, 4, level - 1),
                (3, 4, level - 1), (4, 4, level - 1)]
    if x == 1 and y == 2:
        return [(x - 1, y, level), (x, y+1, level),
                (x, y-1, level), (0, 0, level - 1),
                (0, 1, level - 1), (0, 2, level - 1),
                (0, 3, level - 1), (0, 4, level - 1)]
    if x == 3 and y == 2:
        return [(x + 1, y, level), (x, y+1, level),
                (x, y-1, level), (4, 0, level - 1),
                (4, 1, level - 1), (4, 2, level - 1),
                (4, 3, level - 1), (4, 4, level - 1)]


def doStep(grid):
    nextGrid = defaultdict(int)
    sought = set(grid)
    keys = list(grid.keys())
    for cell in keys:
        neighbourHood = getNeighbourhood(cell)
        if sum(map(lambda x: grid[x], neighbourHood)) == 1:
            nextGrid[cell] = 1
        for adjacentCell in neighbourHood:
            if adjacentCell in sought:
                continue
            liveCells = sum(
                map(lambda x: grid[x], getNeighbourhood(adjacentCell)))
            if liveCells == 1 or liveCells == 2:
                nextGrid[adjacentCell] = 1
            sought.add(adjacentCell)

    return nextGrid


grid = buildGrid(data)
for i in range(200):
    grid = doStep(grid)

print('Assignment 2:', len(grid))
