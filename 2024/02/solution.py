with open("input.txt", "r") as file:
    reports = file.readlines()


def try_reversed(fn):
    def _fn(x):
        return fn(x) or fn(x[::-1])

    return _fn


def safe(levels: list[int]) -> bool:
    return all(0 < (l_j - l_i) < 4 for l_i, l_j in zip(levels, levels[1:]))


levels = [list(map(int, line.split())) for line in reports]


@try_reversed
def dampened(levels: list[int]) -> bool:
    if safe(levels):
        return True

    for i in range(len(levels)):
        test_levels = [level for j, level in enumerate(levels) if j != i]
        if safe(test_levels):
            return True

    return False


@try_reversed
def recursive(levels: list[int]) -> bool:
    for i in range(len(levels) - 1):
        if not 0 < levels[i + 1] - levels[i] < 4:
            test_i = levels[i - 1 : i] + levels[i + 1 :]
            test_j = levels[i : i + 1] + levels[i + 2 :]
            return safe(test_i) or safe(test_j)
    return True


print("Part one")
print(sum(map(try_reversed(safe), levels)))
print("Part two")
print(sum(map(dampened, levels)))
print(sum(map(recursive, levels)))
