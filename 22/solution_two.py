
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
        value = int(mode == "on")
        # if min(px) < -50 or max(px) > 50 or min(py) < -50 or max(py) > 50 or min(pz) < -50 or max(pz) > 50:
        #     print('big skip')
        #     continue
        print(mode, px, py, pz)
        # for x in range(xs, xf+1):
        #     for y in range(ys, yf + 1):
        #         for z in range(zs, zf + 1):
        cube_points = ((x, y, z) for x in range(xs, xf + 1) for y in range(ys, yf + 1) for z in range(zs, zf + 1))
        for point in cube_points:
            points[point] = value
                    # if any(val < -50 or val > 50 for val in (x, y, z)):
                    #     print("skipping")
                    #     continue
                    # points[(x, y, z)] = int(mode == "on")
    


    result = sum(points.values())
    print(f"The solution for {input_file!r} is {result}.")
    return result


def main():
    # test_result = solve("input.test3")
    # test_answer = 2758514936282235
    # assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()