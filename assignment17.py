from intcode import evalProgram, readIntCode
from collections import defaultdict
from util import getBoundingRect

filepath = 'data17.txt'

input = readIntCode(filepath)


def readCamera(prog):
    state = defaultdict(int)
    pos = (0, 0)

    def outp(x):
        nonlocal pos
        if x == 10:
            pos = (0, pos[1] + 1)
        else:
            state[pos] = x
            pos = (pos[0] + 1, pos[1])

    def inp():
        while True:
            return 0
            yield ()
    next(evalProgram(prog, inp, outp))
    return state


def getJunctions(grid):
    scaffolds = [coord for (coord, value) in grid.items() if value == 35]
    junctions = []
    for coord in scaffolds:
        if grid[(coord[0]+1, coord[1])] == 35 and \
                grid[(coord[0]-1, coord[1])] == 35 and \
                grid[(coord[0], coord[1] + 1)] == 35 and \
                grid[(coord[0], coord[1] - 1)] == 35:
            junctions.append(coord)
    return junctions


grid = readCamera(input.copy())
print('Assignment 1:', sum(map(lambda x: x[0] * x[1], getJunctions(grid))))


x1, x2, y1, y2 = getBoundingRect(list(grid.keys()))


for y in range(y1, y2):
    print("".join([chr(grid[(x, y)]) for x in range(x1, x2)]))

robot = next((coord for (coord, value) in grid.items()
              if value in [60, 62, 94, 118]))


turns = {
    'E': {
        'N': 'L',
        'S': 'R'
    },
    'W': {
        'N': 'R',
        'S': 'L'
    },
    'S': {
        'W': 'R',
        'E': 'L'
    },
    'N':  {
        'W': 'L',
        'E': 'R'
    }
}

turnsDir = {
    'E': {
        'L': 'N',
        'R': 'S'
    },
    'W': {
        'L': 'S',
        'R': 'N'
    },
    'S': {
        'L': 'E',
        'R': 'W'
    },
    'N':  {
        'L': 'W',
        'R': 'E'
    }
}

vectors = {
    'E': [1, 0],
    'W': [-1, 0],
    'N': [0, -1],
    'S': [0, 1]
}

caretToDir = {
    60: 'W',
    62: 'E',
    94: 'N',
    118: 'S'
}


def getInstructions(grid, startPos):
    def getTurn(pos, direction):
        if direction == 'E' or direction == 'W':
            if grid[(pos[0]+vectors['N'][0], pos[1] + vectors['N'][1])] == 35:
                return turns[direction]['N']
            if grid[(pos[0]+vectors['S'][0], pos[1] + vectors['S'][1])] == 35:
                return turns[direction]['S']

        if direction == 'N' or direction == 'S':
            if grid[(pos[0]+vectors['W'][0], pos[1] + vectors['W'][1])] == 35:
                return turns[direction]['W']
            if grid[(pos[0]+vectors['E'][0], pos[1] + vectors['E'][1])] == 35:
                return turns[direction]['E']

        print('no moves for pos', pos)

    result = []
    direction = caretToDir[grid[startPos]]
    currentPos = startPos
    steps = 0
    while True:
        nextCell = (currentPos[0] + vectors[direction][0],
                    currentPos[1] + vectors[direction][1])
        if grid[nextCell] != 35:
            turn = getTurn(currentPos, direction)
            if not turn:
                result.append(steps)
                print('done')
                break
            if steps:
                result.append(steps)
            result.append(turn)
            steps = 0
            direction = turnsDir[direction][turn]
        else:
            steps += 1
            currentPos = nextCell
    return result


instructions = getInstructions(grid, robot)


def findPatterns(instructions):
    grouped = [''.join(map(str, instructions[i:i + 2]))
               for i in range(0, len(instructions), 2)]

    ops = set(grouped)
    instr = ''.join(map(str, instructions))
    newInstr = instr
    mapping = {op:  chr(ord('U') + i) for (i, op) in enumerate(ops)}
    reverseMapping = {mapping: op for (op, mapping) in mapping.items()}
    for (op, mapping) in mapping.items():
        newInstr = newInstr.replace(op, mapping)
    patterns = set()
    for i in range(len(newInstr)):
        for j in range(2, 6):
            pattern = str(newInstr[i:i+j])
            if pattern not in patterns and newInstr.count(pattern) > 1:
                patterns.add(pattern)

    for pattern in patterns:
        for pattern2 in patterns:
            if pattern2 == pattern:
                continue
            for pattern3 in patterns:
                if pattern3 == pattern or pattern3 == pattern2:
                    continue
                result = newInstr.replace(pattern, '').replace(
                    pattern2, '').replace(pattern3, '')
                if not result:
                    res1 = ''.join(map(lambda x: reverseMapping[x], pattern))
                    res2 = ''.join(map(lambda x: reverseMapping[x], pattern2))
                    res3 = ''.join(map(lambda x: reverseMapping[x], pattern3))
                    sequence = instr.replace(res1, 'A').replace(
                        res2, 'B').replace(res3, 'C')
                    return res1, res2, res3, sequence


def toOutput(instr):
    result = []
    preDigit = False
    for i in instr:
        if i.isdigit():
            result.append(i)
            preDigit = True
        elif preDigit:
            result.append(',')
            result.append(i)
            result.append(',')
            preDigit = False
        else:
            result.append(i)
            result.append(',')
            preDigit = False
    if result[-1] == ',':
        result[-1] = '\n'
    else:
        result.append('\n')
    return result


(a, b, c, sequence) = findPatterns(instructions)
instr = toOutput(sequence) + toOutput(a) + \
    toOutput(b) + toOutput(c) + ['n', '\n']


def runProgram(prog, instr):
    result = 0
    idx = -1

    def outp(x):
        nonlocal result
        result = x

    def inp():
        nonlocal idx
        while True:
            idx += 1
            return ord(instr[idx])
        yield ()

    next(evalProgram(prog, inp, outp))
    return result


prog = input.copy()
prog[0] = 2
print(runProgram(prog, instr))
