from itertools import product
def start_finish(string):
    start, finish = string[2:].split("..")
    return int(start), int(finish)

def solve(input_file: str) -> int:
    data = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            switch, borders = line.split(" ")
            x1, y1, z1 = borders.split(",")
            xs, xf = start_finish(x1)
            ys, yf = start_finish(y1)
            zs, zf = start_finish(z1)
            data.append([switch, (xs, xf), (ys, yf), (zs, zf)])
    
    points = {(x, y, z): 0 for x in range(-50, 51) for y in range(-50, 51) for z in range(-50, 51)}
    
    for mode, px, py, pz in data:
        xs, xf = px
        ys, yf = py
        zs, zf = pz
        if min(px) < -50 or max(px) > 50 or min(py) < -50 or max(py) > 50 or min(pz) < -50 or max(pz) > 50:
            continue
        value = int(mode == "on")
        updates = {(x, y, z): value for x, y, z in product(range(xs, xf + 1), range(ys, yf + 1), range(zs, zf + 1))}
        points.update(updates)
    


    result = sum(points.values())
    print(f"The solution for {input_file!r} is {result}.")
    return result


def main():
    test_result = solve("input.test")
    test_answer = 39
    assert test_result == test_answer
    test_result = solve("input.test2")
    test_answer = 590784
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()