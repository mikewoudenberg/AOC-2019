import numpy as np
from shapely.geometry import LineString

filepath = 'data3.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


movementVector = {
    'U': np.array([0, 1]),
    'D': np.array([0, -1]),
    'L': np.array([-1, 0]),
    'R': np.array([1, 0])
}


def getCoordinates(moves):
    coordinate = np.array([0, 0])
    coordinates = {}
    steps = 0
    for move in moves:
        movement = movementVector[move[0]]
        for i in range(0, int(move[1:])):
            newCoordinate = coordinate + movement
            steps += 1
            coordinates['{}:{}'.format(
                newCoordinate[0], newCoordinate[1])] = (newCoordinate, steps)
            coordinate = newCoordinate

    return coordinates


lines = readlines('data3.txt')
path1 = getCoordinates(lines[0].split(','))
path2 = getCoordinates(lines[1].split(','))

intersections = [(x, abs(path1[x][0][0]) + abs(path1[x][0][1]), path1[x][1] + path2[x][1]) for x in np.intersect1d(
    list(path1.keys()), list(path2.keys()))]

intersections.sort(key=lambda x: x[1])
print('Assignment 1: ', intersections[0][1])
intersections.sort(key=lambda x: x[2])
print('Assignment 2: ', intersections[0][2])


# cheat mode:
line1 = LineString([x[0] for x in path1.values()])
line2 = LineString([x[0] for x in path2.values()])
intersections = line1.intersection(line2)

print('Assignment 1:', sorted(
    map(lambda x: abs(x.x) + abs(x.y), intersections))[0])
print('Assignment 2:', sorted(
    map(lambda x: 2 + line1.project(x) + line2.project(x), intersections))[0])
