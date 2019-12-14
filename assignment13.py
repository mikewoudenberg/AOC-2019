import curses
from intcode import evalProgram
from util import getBoundingRect
from collections import Counter, defaultdict

filepath = 'data13.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


input = {i: int(x) for i, x in enumerate(readlines(filepath)[0].split(','))}


stdscr = curses.initscr()
codeToScreen = {
    0: '.',
    1: '█',
    2: '▒',
    3: '▄',
    4: 'o'
}


def draw(state):
    x1, x2, y1, y2 = getBoundingRect(list(state.keys()))

    for y in range(y1, y2):

        line = "".join([codeToScreen[state[(x, y)]]
                        for x in range(x1+1, x2)])
        stdscr.addstr(y - y1, 0, line)
    stdscr.refresh()


def playGame(prog):
    state = defaultdict(int)
    coord = []
    ball = (0, 0)
    paddle = (0, 0)

    def getBall():
        return ball

    def outp(x):
        nonlocal coord
        nonlocal ball
        nonlocal paddle
        if len(coord) == 2:
            loc = tuple(coord)
            state[loc] = x
            if x == 4:
                ball = loc
            elif x == 3:
                paddle = loc
                draw(state)
            coord = []

        else:
            coord.append(x)

    def inp():
        nonlocal ball
        nonlocal paddle
        while True:
            if ball[0] > paddle[0]:
                return 1
            elif ball[0] < paddle[0]:
                return -1
            return 0
            yield ()
    next(evalProgram(prog, inp, outp))
    return state


state = playGame(input.copy())
print('Assignment 1: ', Counter(state.values())[2])

state = playGame({**input, 0: 2})
print('Assignment 2: ', state[(-1, 0)])
