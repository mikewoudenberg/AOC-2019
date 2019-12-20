from util import getBoundingRect
import networkx as nx
from collections import defaultdict
import itertools


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def parseMaze(lines):
    state = defaultdict(lambda: '')
    pipes = defaultdict(lambda: set())
    for y, line in enumerate(lines):
        prevPrev = prev = ''
        for x, char in enumerate(line):
            coord = (x, y)
            state[coord] = char
            if prevPrev.isupper() and prev.isupper() and char == '.':
                pipes[prevPrev + prev].add((x, y))
            elif prevPrev == '.' and prev.isupper() and char.isupper():
                pipes[prev + char].add((x-2, y))
            prevPrev = prev
            prev = char

    _, x2, __, y2 = getBoundingRect(list(state.keys()))
    for x in range(x2):
        prev = prevPrev = ''
        for y in range(y2):
            char = state[(x, y)]
            if prevPrev.isupper() and prev.isupper() and char == '.':
                pipes[prevPrev + prev].add((x, y))
            elif prevPrev == '.' and prev.isupper() and char.isupper():
                pipes[prev + char].add((x, y-2))
            prevPrev = prev
            prev = char
    start = list(pipes['AA'])[0]
    end = list(pipes['ZZ'])[0]
    pipes = {pipe: pipes[pipe]
             for pipe in pipes if pipe != 'AA' and pipe != 'ZZ'}
    return state, pipes, start, end


def buildGraph(grid, pipes):
    _, x2, __, y2 = getBoundingRect(list(grid.keys()))
    graph = nx.grid_2d_graph(x2, y2)
    pipecoords = [item for pipe in pipes.values() for item in pipe]
    for coord in (coord for (coord, value) in grid.items() if value != '.'):
        graph.remove_node(coord)
    for coords in (list(coords) for coords in pipes.values() if len(coords) == 2):
        graph.add_edge(coords[0], coords[1])
    return graph


grid, pipes, start, end = parseMaze(readlines('data20.txt'))
graph = buildGraph(grid, pipes)
print('Assignment 1:', nx.shortest_path_length(graph, start, end))

innerPortals = set()
outerPortals = set()
maxX = max(grid.keys(), key=lambda x: x[0])[0]
maxY = max(grid.keys(), key=lambda x: x[1])[1]
for pipe in pipes:
    for coord in pipes[pipe]:
        if coord[0] == 2 or coord[0] == maxX - 2 or \
                coord[1] == 2 or coord[1] == maxY - 2:
            outerPortals.add(coord)
        else:
            innerPortals.add(coord)


def buildFlatGraph(grid, pipes, start, end):
    _, x2, __, y2 = getBoundingRect(list(grid.keys()))
    graph = nx.grid_2d_graph(x2, y2)
    for coord in (coord for (coord, value) in grid.items() if value != '.'):
        graph.remove_node(coord)
    paths = {}
    stuff = list(pipes.values())
    stuff.append([start, end])
    for (coord1, coord2) in itertools.combinations((coord for pipe in stuff for coord in pipe), 2):
        try:
            length = nx.shortest_path_length(graph, coord1, coord2)
            paths[(coord1, coord2)] = length
            paths[(coord2, coord1)] = length
        except nx.NetworkXNoPath:
            pass

    return graph, paths


def findReachableCoords(coord, paths, level=0):
    for (coord1, coord2) in paths:
        if coord1 != coord:
            continue
        if level == 0 and (coord2 in innerPortals or coord2 == end):
            yield (coord2, 1, paths[(coord1, coord2)] + 1)
        if level > 0 and (coord2 != start and coord2 != end):
            yield (coord2, 1 if coord2 in innerPortals else -1, paths[(coord1, coord2)] + 1)


graph, paths = buildFlatGraph(grid, pipes, start, end)
jumps = {}
for pipe in map(list, pipes.values()):
    jumps[pipe[0]] = pipe[1]
    jumps[pipe[1]] = pipe[0]


def search():
    result = []
    workQueue = [(start, 0, 0)]
    minPathLength = None
    cache = {}
    while workQueue:
        coord, pathLength, level = workQueue.pop()
        if minPathLength and pathLength >= minPathLength:
            continue

        reachableCoords = list(findReachableCoords(coord, paths, level))

        if level == 0 and end in map(lambda x: x[0], reachableCoords):
            addedPathLength = [addedPathLength for (
                newCoord, _, addedPathLength) in reachableCoords if newCoord == end][0]
            minPathLength = pathLength + addedPathLength - 1
            result.append(minPathLength)
            continue
        key = (coord, level)
        if key in cache:
            l = cache[key]
            if pathLength >= l:
                continue
        cache[key] = pathLength
        for (newCoord, levelChange, addedPathLength) in reachableCoords:
            workQueue.append(
                (jumps[newCoord], pathLength + addedPathLength, level+levelChange))

    return result


print('Assignment 2:', min(search()))
