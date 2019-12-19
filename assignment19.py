from intcode import readIntCode, runProgram
from timeit import timeit
inputFile = 'data19.txt'

prog = readIntCode(inputFile)


def beam(prog, x, y):
    _, stdout = runProgram(prog.copy(), [x, y])
    return stdout[0]


@timeit
def runBeam(prog, maxX, maxY):
    affected = [[0 for x in range(maxX)] for y in range(maxY)]

    for x in range(maxX):
        for y in range(maxY):
            affected[y][x] = beam(prog, x, y)
    return affected


affected = runBeam(prog, 50, 50)
for y in range(50):
    print(''.join(['#' if affected[y][x] == 1 else '.' for x in range(50)]))


print('Assignment 1:', sum((affected[y][x]
                            for x in range(50) for y in range(50))))

# based n the slopes of the beam we can skip anything before the given coords (just make sure the coords are left of the beam ;))
x, y = 700, 1000
while True:
    if beam(prog, x, y) == 1:
        if beam(prog, x+99, y-99) == 1:
            print(x*10000 + (y-99))
            break
        else:
            y += 1
    else:
        x += 1
