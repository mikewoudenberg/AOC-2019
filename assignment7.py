import itertools
import queue
from intcode import evalProgram, readIntCode, runProgram

filepath = 'data7.txt'


input = readIntCode(filepath)

signal = 0
for ampSettings in itertools.permutations([0, 1, 2, 3, 4]):
    stdin = [0]
    for ampSetting in ampSettings:
        stdin.insert(0, int(ampSetting))
        (_, stdout) = runProgram(input.copy(), stdin)
        stdin.append(stdout[0])
    if stdout[0] > signal:
        signal = stdout[0]

print('Assignment 1:', signal)


def run_amp(inqueue, outqueue):
    def outp(x):
        outqueue.put_nowait(x)

    def inp():
        while True:
            try:
                return inqueue.get_nowait()
            except queue.Empty:
                pass
            yield ()
    return evalProgram(input.copy(), inp, outp)


max_output = 0
for ordering in itertools.permutations([5, 6, 7, 8, 9]):
    queues = [queue.Queue() for _ in range(6)]
    for (ique, order) in zip(queues, ordering):
        ique.put(order)
    queues[0].put(0)
    coroutines = []
    for idx in range(5):
        coroutines.append(run_amp(queues[idx], queues[(idx + 1) % 5]))
    for _ in itertools.zip_longest(*coroutines):
        pass
    last_out = queues[0].get_nowait()
    max_output = max(max_output, last_out)

print('Assignment 2:', max_output)
