from collections import defaultdict

EXAMPLE = "example.txt"
INPUT = "input.txt"
FILENAME = EXAMPLE

Game = tuple[str, str, str]

CHIEF_IDENTIFIER = "t"


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    network_map = parse(FILENAME)
    games = find_games(network_map)
    narrowed = narrow_games(games, CHIEF_IDENTIFIER)
    result = len(narrowed)
    print(f"Part one: {result}")


def part_two() -> None:
    network_map = parse(FILENAME)
    cliques = find_cliques(network_map)
    print(cliques)
    result = None
    print(f"Part two: {result}")


def find_games(network_map: dict[str, set[str]]) -> set[Game]:
    games = set[Game]()
    for name_1, conns_1 in network_map.items():
        for name_2 in conns_1:
            conns_2 = network_map[name_2]
            common = conns_1 & conns_2
            for name_3 in common:
                game_id = identify_game(name_1, name_2, name_3)
                if game_id not in games:
                    games.add(game_id)
    return games


def identify_game(name_1: str, name_2: str, name_3: str) -> Game:
    return tuple(sorted([name_1, name_2, name_3]))


def narrow_games(games: set[Game], identifier: str) -> set[Game]:
    result = {
        game for game in games if any(name.startswith(identifier) for name in game)
    }
    return result


def find_cliques(
    network_map: dict[str, set[str]], clique_ids: set[str] | None = None
) -> set[set[str]]:
    if clique_ids is None:
        clique_ids = set[str]()
        for name1, conns in network_map.items():
            clique_ids |= {identify_clique({name1, name2}) for name2 in conns}
    cliques = {tuple(make_clique(clique_id)) for clique_id in clique_ids}
    print(cliques)


def identify_clique(clique: set[str]) -> str:
    result = ",".join(sorted(clique))
    return result


def make_clique(clique_id: str) -> tuple[str]:
    result = tuple(clique_id.split(","))
    return result


def largest_clique(network_map: dict[str, set[str]]) -> int:
    pass


def parse(filename: str) -> dict[str, set[str]]:
    network_map = defaultdict(set)
    with open(filename, "r") as file:
        for line in file:
            [c1, c2] = line.strip().split("-")
            network_map[c1].add(c2)
            network_map[c2].add(c1)
    return network_map


def build_adj_matrix(network_map: dict[str, set[str]]) -> dict[str, dict[str, int]]:
    matrix = {name: {} for name in network_map}
    for name1, conns in network_map.items():
        for name2 in conns:
            matrix[name1][name2] = 1
            matrix[name2][name1] = 1
    return matrix


if __name__ == "__main__":
    main()
