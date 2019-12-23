from threading import Thread
from queue import Empty, Queue
from intcode import readIntCode, evalProgram
import time

prog = readIntCode('data23.txt')


def runComputer(prog, nr, network):
    buffer = []
    writeBuffer = [nr]
    valueOfNAT = None
    sentValue = None

    def outp(x):
        nonlocal buffer
        nonlocal valueOfNAT
        buffer.append(x)
        if len(buffer) == 3:
            if buffer[0] == 255:
                if not valueOfNAT:
                    print('Assignment 1:', buffer[2])
                newValue = tuple(buffer[1:])
                valueOfNAT = newValue
            else:
                network[buffer[0]].put(tuple(buffer[1:]))
            buffer = []

    def inp():
        nonlocal valueOfNAT
        nonlocal sentValue
        while True:
            if writeBuffer:
                return writeBuffer.pop(0)
            try:
                res = network[nr].get_nowait()
                writeBuffer.extend(res)
                return writeBuffer.pop(0)
            except Empty:
                if valueOfNAT and sum(map(lambda x: x.qsize(), network.values())) == 0:
                    network[0].put(valueOfNAT)
                    if sentValue == valueOfNAT:
                        print('Assignment 2:', valueOfNAT[1])
                    sentValue = valueOfNAT
                time.sleep(0)
                return -1

            yield ()

    next(evalProgram(prog, inp, outp))


def simulate(prog, nrOfComputers):
    network = {i: Queue() for i in range(nrOfComputers)}
    threads = [Thread(target=runComputer, args=(prog.copy(), i, network))
               for i in range(nrOfComputers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


simulate(prog, 50)
