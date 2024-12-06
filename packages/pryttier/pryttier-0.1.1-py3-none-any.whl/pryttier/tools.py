from functools import partial
from typing import *


class Infix(object):
    def __init__(self, func: Callable) -> None:
        self.func = func

    def __or__(self, other: Self) -> Self:
        return self.func(other)

    def __ror__(self, other: Self) -> Self:
        return Infix(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)


# ===Some Infix Operations===
percentOf = Infix(lambda x, y: x / 100 * y)  # checks x% of y
isDivisibleBy = Infix(lambda x, y: x % y == 0)  # checks if x is divisible by y

# x is the function to apply and y is the iterator for the function to be applied on
applyTo = Infix(lambda x, y: [x(i) for i in y])


def apply(itr: Iterable, func: Callable) -> list:
    return [func(x) for x in itr]


def apply2D(iter1: Sequence, iter2: Sequence, func: Callable) -> list:
    return [func(item1, item2) for item1, item2 in zip(iter1, iter2)]


def chunks(lst: MutableSequence, n: int):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result


def findCommonItems(*lsts: list) -> list:
    return list(set(lsts[0]).intersection(*lsts[1:]))


def swap(array: list, index1: int, index2: int):
    temp: int = array[index1]
    array[index1] = array[index2]
    array[index2] = temp


def listPrint(arr: list, end: str = " "):
    for i in arr:
        print(i, end=end)