from parse import parse


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


shuffle = readlines('data22.txt')


def doShuffle(shuffle, cards):
    for move in shuffle:
        res = parse('cut {:d}', move)
        if res:
            cards = cards[res[0]:] + cards[:res[0]]
            continue
        res = parse('deal with increment {:d}', move)
        if res:
            newCards = {0: cards[0]}
            idx = 0
            for card in cards[1:]:
                idx += res[0]
                newCards[idx % len(cards)] = card
            cards = [newCards[i] for i in range(len(cards))]
            continue
        if move == 'deal into new stack':
            cards = cards[::-1]
            continue
        print('Unknown move', move)
    return cards


cards = doShuffle(shuffle, [i for i in range(10007)])
print('Assignment 1:', cards.index(2019))
cards = doShuffle(shuffle, cards)
print('Assignment 2:', cards.index(2019))
