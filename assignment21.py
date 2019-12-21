from intcode import evalProgram, readIntCode

prog = readIntCode('data21.txt')
# regs A,B,C,D True if ground
# regs J,T J=jump if true, T temporal storage
# ops AND OR NOT. 2nd argument must be J or T


def runJumper(prog, instr):
    pos = 0
    idx = -1
    stdout = None

    def outp(x):
        nonlocal stdout
        if x > 255:
            stdout = x
        else:
            print(chr(x), end='')

    def inp():
        nonlocal idx
        while idx < len(instr):
            idx += 1
            return ord(instr[idx])
            yield ()
    next(evalProgram(prog, inp, outp))
    return stdout


####
# Only jump when D = true
# jump when A or B or C is false
# NOT (A AND B AND C) AND D
# x =  A AND B
# y = x AND C
# z = !y
# J = D AND z

instr = """OR A T
AND B T
AND C T
NOT T J
AND D J
WALK
"""
print('Assignment 1:', runJumper(prog.copy(), instr))


instr = """OR A T
AND B T
AND C T
NOT T J
AND D J
NOT E T
NOT T T
OR  H T
AND T J
RUN
"""
print('Assignment 2:', runJumper(prog.copy(), instr))
