import re
import itertools
import math
filename = 'data12.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def getMoons(lines):
    result = []
    vector = None

    for line in lines:
        (x, y, z) = re.match(
            r"<x=([^,]+), y=([^,]+), z=([^,]+)>", line).groups()
        result.append([int(x), int(y), int(z), 0, 0, 0])

    return result


def energyInSystem(moons):
    totalEnergy = 0
    for moon in moons:
        totalEnergy += (abs(moon[0]) + abs(moon[1]) + abs(moon[2])) * \
            (abs(moon[3]) + abs(moon[4]) + abs(moon[5]))
    return totalEnergy


def simulate(moons, dim):
    for (moon, otherMoon) in itertools.combinations(range(len(moons)), 2):
        if moons[moon][dim] < moons[otherMoon][dim]:
            moons[moon][dim + 3] += 1
            moons[otherMoon][dim + 3] -= 1
        elif moons[moon][dim] > moons[otherMoon][dim]:
            moons[moon][dim + 3] -= 1
            moons[otherMoon][dim + 3] += 1
    for moon in moons:
        moon[dim] += moon[dim+3]


def iterate(moons, steps):
    for dim in range(3):
        for i in range(steps):
            simulate(moons, dim)


def findCycles(moons, steps):
    cycles = []
    for j in range(3):
        projections = set()
        for i in range(steps):
            simulate(moons, j)
            projection = tuple([(moon[j], moon[j+3])
                                for moon in moons])
            if projection in projections:
                cycles.append(i)
                if len(cycles) == 3:
                    return cycles
                break
            projections.add(projection)


moons = getMoons(readlines('data12.txt'))
iterate(moons.copy(), 1000)
print('Assignment 1:', energyInSystem(moons))


def lcm(a, b):
    return (a*b) // math.gcd(a, b)


cycles = findCycles(moons.copy(), 10000000)
print('Assignment 2:', lcm(lcm(cycles[0], cycles[1]), cycles[2]))
