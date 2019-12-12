import re
import numpy as np
import itertools
filename = 'data12.txt'


class Moon:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = np.zeros(3)

    def __str__(self):
        return "{}: {}".format(str(self.position), str(self.velocity))


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def getMoons(lines):
    result = []
    vector = None

    for line in lines:
        (x, y, z) = re.match(
            r"<x=([^,]+), y=([^,]+), z=([^,]+)>", line).groups()
        result.append(Moon((int(x), int(y), int(z))))

    return result


def energyInSystem(moons):
    totalEnergy = 0
    for moon in moons:
        totalEnergy += (np.sum(np.absolute(moon.position))
                        * np.sum(np.absolute(moon.velocity)))
    return totalEnergy


def simulate(moons, steps):
    projections = [set(), set(), set()]
    dimensionsToLookFor = [0, 1, 2]

    def updateVelocity(moons):
        for (moon, otherMoon) in itertools.combinations(moons, 2):
            signs = [np.sign(x-y)
                     for (x, y) in zip(otherMoon.position, moon.position)]
            moon.velocity += signs
            otherMoon.velocity -= signs

    def updatePosition(moon):
        moon.position = moon.position + moon.velocity

    cycles = []

    for i in range(steps):
        updateVelocity(moons)
        for moon in moons:
            updatePosition(moon)

        for dim in dimensionsToLookFor:
            projection = tuple([(moon.position[dim], moon.velocity[dim])
                                for moon in moons])
            if projection in projections[dim]:
                cycles.append(i)
                if len(cycles) == 3:
                    return cycles
                dimensionsToLookFor.remove(dim)
            projections[dim].add(projection)


moons = getMoons(readlines('data12.txt'))
simulate(moons.copy(), 1000)
print('Assignment 1:', energyInSystem(moons))

cycles = simulate(moons.copy(), 10000000)
print('Assignment 2:', np.lcm.reduce(cycles))
