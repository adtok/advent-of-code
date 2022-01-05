KEY = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def get_intersection(i, j):
    s1 = set(KEY[i])
    s2 = set(KEY[j])
    return len(s1.intersection(s2))


uniques = [1, 4, 7, 8]
len_5 = [2, 3, 5]
len_6 = [0, 6, 9]


print(" | 1| 4| 7| 8")
print("-+--+--+--+--")
for search in len_5 + len_6:
    result = "|".join(f" {get_intersection(search, unique)}" for unique in uniques)
    print(f" {search}|{result}")
        