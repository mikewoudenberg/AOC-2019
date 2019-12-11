def runProgram(prog, stdin=[]):
    stdout = []

    def outp(x):
        stdout.append(x)

    def inp():
        while True:
            return stdin.pop(0)
            yield ()

    return (next(evalProgram(prog.copy(), inp, outp)), stdout)


def getParam(prog, idx, paramMode, relativeBase):
    val = prog.get(idx, 0)
    if paramMode == 0:
        return prog.get(val, 0)
    if paramMode == 1:
        return val
    if paramMode == 2:
        return prog.get(val + relativeBase, 0)
    print('Unknown param mode')


def setParam(prog, idx, paramMode, set_to, relativeBase):
    val = prog.get(idx, 0)
    if paramMode == 0:
        prog[val] = set_to
        return
    if paramMode == 2:
        prog[val + relativeBase] = set_to
        return
    print('Unknown param mode')


def decode(instruction):
    return (instruction % 100,
            (instruction // 100) % 10,
            (instruction // 1000) % 10,
            (instruction // 10000) % 10)


def evalProgram(prog, inp, outp):
    idx = 0
    relativeBase = 0
    while True:
        (op, paramMode1, paramMode2, paramMode3) = decode(prog[idx])
        if op == 1:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            p2 = getParam(prog, idx + 2, paramMode2, relativeBase)
            setParam(prog, idx + 3, paramMode3, p1 + p2, relativeBase)
            idx += 4
        elif op == 2:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            p2 = getParam(prog, idx + 2, paramMode2, relativeBase)
            setParam(prog, idx + 3, paramMode3, p1 * p2, relativeBase)
            idx += 4
        elif op == 3:
            x = yield from inp()
            setParam(prog, idx + 1, paramMode1, x, relativeBase)
            idx += 2
        elif op == 4:
            outp(getParam(prog, idx + 1, paramMode1, relativeBase))
            idx += 2
        elif op == 5:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            if p1:
                idx = getParam(prog, idx + 2, paramMode2, relativeBase)
            else:
                idx += 3
        elif op == 6:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            if not p1:
                idx = getParam(prog, idx + 2, paramMode2, relativeBase)
            else:
                idx += 3
        elif op == 7:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            p2 = getParam(prog, idx + 2, paramMode2, relativeBase)
            setParam(prog, idx + 3, paramMode3,
                     1 if p1 < p2 else 0, relativeBase)
            idx += 4
        elif op == 8:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            p2 = getParam(prog, idx + 2, paramMode2, relativeBase)
            setParam(prog, idx + 3, paramMode3,
                     1 if p1 == p2 else 0, relativeBase)
            idx += 4
        elif op == 9:
            p1 = getParam(prog, idx + 1, paramMode1, relativeBase)
            relativeBase += p1
            idx += 2
        elif op == 99:
            idx += 1
            break
        else:
            print("BAD CODE %d AT %d" % (prog[idx], idx))
            break
    yield prog[0]
