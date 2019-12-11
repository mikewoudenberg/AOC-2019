import re
input = range(402328, 864247)


def neverDecreases(number):
    digits = list(number)
    digits.sort()
    return number == ''.join(digits)


def hasDoubleDigit(number):
    return len(set(number)) != len(list(number))


def containsRepeatingExactlyTwice(number):
    currentDigit = number[0]
    next = 1
    length = 1

    while(next < len(number)):
        nextDigit = number[next]
        if (nextDigit == currentDigit):
            length += 1
        elif length == 2:
            return True
        else:
            length = 1
            currentDigit = nextDigit
        next += 1

    return length == 2


keys = [x for x in input if neverDecreases(str(x)) and hasDoubleDigit(str(x))]
print('Assignment 1:', len(keys))

validKeys = [x for x in keys if containsRepeatingExactlyTwice(str(x))]
print('Assignment 2:', len(validKeys))


# cheat mode
def regexFoo(number):
    result = re.search(
        r"([0-9])(?!\1)(.)\2(?!\1)(?!\2)|^([0-9])\3(?!\3)", number)
    return result


validKeys = [x for x in keys if regexFoo(str(x))]
print('Assignment 2:', len(validKeys))
