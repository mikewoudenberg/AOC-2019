import re
import networkx as nx
from util import getBoundingRect
from networkx.exception import NetworkXNoPath
import itertools
inputFile = 'data18.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def parseMaze(lines):
    state = {}
    keys = {}
    entry = (0, 0)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            coord = (i, j)
            state[coord] = char
            if char == '@':
                entry = coord
            elif char.islower():
                keys[char] = coord
    return state, keys, entry


def buildGraph(grid):
    _, x2, __, y2 = getBoundingRect(list(grid.keys()))
    graph = nx.grid_2d_graph(x2, y2)
    for coord in (coord for (coord, value) in grid.items() if value == '#'):
        graph.remove_node(coord)
    return graph


def findReachableKeys(grid, paths, keys, coord, collectedKeys):
    result = []
    allowed = set(k.upper() for k in collectedKeys) | \
        set('@.abcdefghijklmnopqrstuvwxyz')
    for k in set(keys.keys()) - set(collectedKeys):
        path = paths[(coord, keys[k])]
        if all(map(lambda x: grid[x] in allowed, path)):
            result.append((k, keys[k], len(path) - 1))
    return result


def buildPaths(graph, keys, entry):
    paths = {}
    allKeys = {**keys, '@': entry}
    for (key1, key2) in itertools.combinations(allKeys, 2):
        path = nx.shortest_path(graph, allKeys[key1], allKeys[key2])
        paths[(allKeys[key1], allKeys[key2])] = path
        paths[(allKeys[key2], allKeys[key1])] = path[::-1]
    return paths


(grid, keys, entry) = parseMaze(readlines(inputFile))
graph = buildGraph(grid)
paths = buildPaths(graph, keys, entry)


def shortestPaths(entry, grid, paths, allKeys):
    result = []
    workQueue = [(entry, 0, ())]
    minPathLength = None
    cache = {}
    while workQueue:
        coord, pathLength, keys = workQueue.pop()
        if minPathLength and pathLength >= minPathLength:
            continue
        if len(keys) == 26:
            minPathLength = pathLength
            result.append(pathLength)
            continue
        key = (coord, ''.join(sorted(keys)))
        if key in cache:
            l, res = cache[key]
            if l <= pathLength:
                continue
        else:
            res = sorted(findReachableKeys(
                grid, paths, allKeys, coord, keys), key=lambda r: r[2], reverse=True)
        cache[key] = pathLength, res
        for k, p, m in res:
            workQueue.append((p, pathLength + m, keys + (k,)))
    return result


print('Assignment 1:', min(
    length for length in shortestPaths(entry, grid, paths, keys)))

newGrid = grid.copy()
newGraph = graph.copy()
starts = []
for i in range(-1, 2):
    for j in range(-1, 2):
        symbol = None
        coord = (entry[0] + i, entry[1] + j)
        if abs(i) == abs(j) and abs(i) == 1:
            symbol = '@'
            starts.append(coord)
        else:
            symbol = '#'
            newGraph.remove_node(coord)
        newGrid[coord] = symbol


sub_graphs = [newGraph.subgraph(c) for c in nx.connected_components(newGraph)]

robots = []
for start in starts:
    robotGraph = next((g for g in sub_graphs if start in g.nodes))
    robotKeys = {k: keys[k] for k in keys if keys[k] in robotGraph.nodes}
    robotPaths = buildPaths(robotGraph, robotKeys, start)
    robots.append((robotKeys, robotPaths))


def shortestPathsMulti(starts, robots, grid):
    result = []
    workQueue = [(tuple(starts), 0, ())]
    minPathLength = None
    cache = {}
    while workQueue:
        coords, pathLength, keys = workQueue.pop()
        if minPathLength and pathLength >= minPathLength:
            continue
        if len(keys) == 26:
            minPathLength = pathLength
            result.append(pathLength)
            continue
        key = (coords, ''.join(sorted(keys)))
        if key in cache:
            l, res = cache[key]
            if l <= pathLength:
                continue
        else:
            res = []
            for i, coord in enumerate(coords):
                robotKeys, robotPaths = robots[i]
                reachableKeys = sorted(findReachableKeys(grid, robotPaths, robotKeys,
                                                         coord, keys), key=lambda r: r[2], reverse=True)
                for reachableKey in reachableKeys:
                    res.append((i,) + reachableKey)
        cache[key] = pathLength, res
        for i, k, p, m in res:
            nposs = coords[:i] + (p,) + coords[i + 1:]
            workQueue.append((nposs, pathLength + m, keys + (k,)))
    return result


print('Assignment 2:', min(
    length for length in shortestPathsMulti(starts, robots, grid)))
