import numpy as np
import math
filePath = 'data10.txt'


class Meteor:
    def __init__(self, coord):
        self.coord = coord
        self.visibleMeteorCount = 0

    def __str__(self):
        return '{}: [{}]'.format(self.coord, self.visibleMeteorCount)


def length(x):
    return (x[0] ** 2 + x[1] ** 2) ** 0.5


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def getMeteors(lines):
    meteors = {}
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                meteors[(j, i)] = Meteor((j, i))
    return meteors


def getVectorsTo(meteor, meteors):
    return [(coord[0] - meteor.coord[0], coord[1] - meteor.coord[1]) for coord in meteors]


def getUnreachables(vectors):
    unreachable = set()
    for i, vector in enumerate(vectors):
        for v in vectors[i+1:]:
            if v in unreachable:
                continue
            scalar = 0
            if v[0] == 0 and vector[0] == 0 and np.sign(v[1]) == np.sign(vector[1]):
                unreachable.add(v)
                continue
            elif v[1] == 0 and vector[1] == 0 and np.sign(v[0]) == np.sign(vector[0]):
                unreachable.add(v)
                continue
            elif v[0] == 0 or v[1] == 0 or vector[0] == 0 or vector[1] == 0:
                continue
            else:
                scalar0 = v[0] / vector[0]
                scalar1 = v[1] / vector[1]
                if scalar0 == scalar1 and scalar0 > 0 and scalar1 > 0:
                    unreachable.add(v)
    return unreachable


meteors = getMeteors(readlines(filePath))


def updateWithReachableCount(meteors):
    for meteor in meteors.values():
        vectors = sorted(getVectorsTo(meteor, meteors),
                         key=length)[1:]

        unreachable = getUnreachables(vectors)
        meteor.visibleMeteorCount = (len(vectors) - len(unreachable))


updateWithReachableCount(meteors)
monitoringStation = sorted(meteors.values(),
                           reverse=True, key=lambda x: x.visibleMeteorCount)[0]
print('Assignment 1:', monitoringStation.visibleMeteorCount)


def getAngle(vector):
    return (math.atan2(vector[1], vector[0]) + 2.5 * math.pi) % (2.0 * math.pi)


def spin(centre, meteors):
    vectors = sorted(getVectorsTo(centre, meteors),
                     key=length)[1:]

    result = []
    while any(vectors):
        unreachable = getUnreachables(sorted(vectors, key=length))
        byAngle = sorted(set(vectors) - unreachable,
                         key=getAngle)
        result.extend([(centre.coord[0] + v[0], centre.coord[1] + v[1])
                       for v in byAngle])
        vectors = unreachable
    return result


killOrder = spin(monitoringStation, meteors)
print('Assignment 2:',  100 * killOrder[199][0] + killOrder[199][1])
