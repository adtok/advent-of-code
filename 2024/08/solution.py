FILENAME = "input.txt"

Point = tuple[int, int]

grid: dict[Point, str] = {}
with open(FILENAME, "r") as file:
    for row, line in enumerate(file):
        for col, frequency in enumerate(line.strip()):
            coordinate = (row, col)
            grid[coordinate] = frequency
            if frequency == ".":
                continue

width = max(grid, key=lambda x: x[0])[0] + 1
height = max(grid, key=lambda x: x[1])[1] + 1

antennas: dict[str, list[Point]] = {}
for coordinate, frequency in grid.items():
    if frequency == ".":
        continue
    if frequency not in antennas:
        antennas[frequency] = []
    antennas[frequency].append(coordinate)


antinodes: set[Point] = set()
for frequency, coordinates in antennas.items():
    length = len(coordinates)
    if length < 2:
        continue
    for i in range(length - 1):
        for j in range(i + 1, length):
            x_0, y_0 = antenna_0 = coordinates[i]
            x_1, y_1 = antenna_1 = coordinates[j]
            antinodes.add(antenna_0)
            antinodes.add(antenna_1)
            dx = x_1 - x_0
            dy = y_1 - y_0
            antinode_0 = (x_0, y_0)
            while (antinode_0 := (antinode_0[0] - dx, antinode_0[1] - dy)) in grid:
                antinodes.add(antinode_0)
            antinode_1 = (x_1, y_1)
            while (antinode_1 := (antinode_1[0] + dx, antinode_1[1] + dy)) in grid:
                antinodes.add(antinode_1)

print(len(antinodes))
