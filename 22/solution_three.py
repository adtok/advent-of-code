from itertools import product

def start_finish(string):
    start, finish = string[2:].split("..")
    return int(start), int(finish)


def get_subrange(cube_range, low, high):
    c0 = cube_range[0]
    c1 = cube_range[-1]
    if c1 < low:
        return []
    elif c0 > high:
        return []
    c0 = max(c0, low)
    c1 = max(c1, low)
    c0 = min(c0, high)
    c1 = min(c1, high)
    return range(c0, c1+1)


def count_uninterrupted(item, rest):
    _, xr, yr, zr = item
    total = len(xr) * len(yr) * len(zr)

    conflicts = []
    ref_val = 0

    for item in rest:
        state, xr2, yr2, zr2 = item
        cxr = get_subrange(xr2, xr[0], xr[-1])
        cyr = get_subrange(yr2, yr[0], yr[-1])
        czr = get_subrange(zr2, zr[0], zr[-1])

        if len(cxr) == 0 or len(cyr) == 0 or len(czr) == 0:
            continue

        conflicts.append((state, cxr, cyr, czr))
        ref_val += len(cxr) + len(cyr) + len(czr)

    
    for idx, item in enumerate(conflicts):
        total -= count_uninterrupted(item, conflicts[idx+1:])

    return total


def solve(input_file: str) -> int:
    data = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            switch, borders = line.split(" ")
            x1, y1, z1 = borders.split(",")
            xs, xf = start_finish(x1)
            ys, yf = start_finish(y1)
            zs, zf = start_finish(z1)
            value = int(switch == "on")
            print(value, (xs, xf), (ys, yf), (zs, zf))
            xrange = range(xs, xf + 1)
            yrange = range(ys, yf + 1)
            zrange = range(zs, zf + 1)
            data.append([switch, xrange, yrange, zrange])

    answer = 0

    for idx, item in enumerate(data):
        state, xr, yr, zr = item
        if state == "off":
            continue
        answer += count_uninterrupted(item, data[idx+1:])
            
    


    result = answer
    print(f"The solution for {input_file!r} is {result}.")
    return result


def main():
    # test_result = solve("input.test3")
    # test_answer = 2758514936282235
    # assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()