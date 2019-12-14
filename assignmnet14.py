import re
import math
from collections import Counter, defaultdict


class Rule:
    def __init__(self, name, arity, constituents):
        self.name = name
        self.arity = arity
        self.constituents = constituents

    def __str__(self):
        return '{} {} requires {}'.format(self.arity, self.name, ''.join(map(str, self.constituents)))


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


def parseComponent(component):
    [count, name] = re.match(r"(\d+) ([A-Z]+)", component).groups()
    return (int(count), name)


def buildRules(lines):
    result = {}
    comps = set()
    for line in lines:
        [ingredients, product] = line.split(' => ')
        (count, name) = parseComponent(product)

        result[name] = Rule(name, count, list(
            map(parseComponent, ingredients.split(', '))))

    return result


rules = buildRules(readlines('data14.txt'))


storage = defaultdict(int)


def getOre(comp, quantity):
    multiplier = math.ceil(quantity / comp.arity)
    result = 0

    storage[comp.name] = storage.get(
        comp.name, 0) + (multiplier * comp.arity - quantity)
    for (count, name) in comp.constituents:
        if name == 'ORE':
            required = count * multiplier
            result += required
        else:
            required = multiplier * count
            stored = storage[name]
            if stored >= required:
                storage[name] = stored - required
            else:
                required -= stored
                storage[name] = 0

                result += getOre(rules[name], required)

    return result


print('Assignment 1:', getOre(rules['FUEL'], 1))
maxOre = 1000000000000
for i in range(1376630, 1376633):
    storage = defaultdict(int)
    if getOre(rules['FUEL'], i) > maxOre:
        print('Assignment 2:', i-1)
        break
