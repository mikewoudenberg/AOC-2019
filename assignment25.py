from intcode import evalProgram, readIntCode

prog = readIntCode('data25.txt')


def doMaze(prog, steps=""):
    nav = []
    buffer = [char for char in steps]

    def inp():
        while True:
            if buffer:
                return ord(buffer.pop(0))
            else:
                command = input('What is thy bidding? ')
                nav.append(command)
                buffer.extend(command)
                buffer.append('\n')
                return ord(buffer.pop(0))
            yield ()

    def outp(x):
        print(chr(x), end='')

    next(evalProgram(prog, inp, outp))
    print('\n'.join(nav))


actions = """south
take astronaut ice cream
north
east
take mouse

north
take spool of cat6
west
north
south
east
north
take hypercube
east
take sand
south
take antenna
north
west
south
south
south
take mutex
south
north
west
take boulder
west
east
south
south
south
west
south
south
south
drop mutex
drop spool of cat6
drop hypercube
drop antenna
south
"""

doMaze(prog, actions)
