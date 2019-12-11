import numpy as np
import networkx as nx
filepath = 'data6.txt'


class Planet:
    def __init__(self, name):
        self.name = name
        self.orbitingPlanets = list()
        self.distanceToCom = 0

    def __str__(self):
        return '{}: [{}]'.format(self.name, ','.join(map(str, self.orbitingPlanets)))


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def buildGraph(pairs):
    planets = {}
    for center, orbit in pairs:
        planet = planets.get(center, Planet(center))
        orbitingPlanet = planets.get(orbit, Planet(orbit))
        planet.orbitingPlanets.append(orbitingPlanet)
        planets[center] = planet
        planets[orbit] = orbitingPlanet

    return planets


pairs = [x.split(')') for x in readlines(filepath)]
planets = buildGraph(pairs)


def dft(currentPlanet, level=0):
    currentPlanet.distanceToCom = level
    for planet in currentPlanet.orbitingPlanets:
        dft(planet, level + 1)


def pathToPlanet(name, currentPlanet):
    if currentPlanet.name == name:
        return [currentPlanet]
    for planet in currentPlanet.orbitingPlanets:
        path = pathToPlanet(name, planet)
        if path:
            return [currentPlanet] + path


dft(planets['COM'])
print('Assignment 1: ', sum(map(lambda x: x.distanceToCom, planets.values())))

pathToSan = pathToPlanet('SAN', planets['COM'])
pathToYou = pathToPlanet('YOU', planets['COM'])

print('Assignment 2', planets['SAN'].distanceToCom-1 + planets['YOU'].distanceToCom-1 - 2 * (next(x[0] for x in zip(pathToSan, pathToYou)
                                                                                                  if x[0] != x[1]).distanceToCom - 1))

# cheat mode:
G = nx.Graph()
G.add_edges_from(pairs)
print('Assignment 1:', sum(nx.single_source_shortest_path_length(G, 'COM').values()))
print('Assignment 2:', nx.shortest_path_length(G, source='SAN', target='YOU')-2)
