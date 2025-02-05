from collections import defaultdict

with open("input.txt", "r") as file:
    [raw_rules, raw_updates] = file.read().split("\n\n")
rule_pairs = map(lambda x: map(int, x.split("|")), raw_rules.split())

updates = list(map(lambda x: list(map(int, x.split(","))), raw_updates.split()))

# print(updates)


rules = defaultdict(set)

for x, y in rule_pairs:
    rules[y].add(x)


def valid(update: list[int], rules: dict[int, set[int]]) -> bool:
    seen = set()
    page_numbers = set(update)
    for page_number in update:
        seen.add(page_number)
        requirements = rules[page_number]
        if any(
            requirement in page_numbers and requirement not in seen
            for requirement in requirements
        ):
            return False
    return True


def middle_page(update: list[int]) -> int:
    return update[len(update) // 2]


print(sum(map(middle_page, filter(lambda x: valid(x, rules), updates))))


def reorder(update: list[int], all_rules: dict[int, set[int]]) -> list[int]:
    page_numbers = set(update)
    rules = {
        page_number: set(filter(lambda r: r in page_numbers, all_rules[page_number]))
        for page_number in update
    }
    new_order = []
    while len(new_order) != len(update):
        for i in page_numbers:
            requirements = rules[i]
            if i not in new_order and all(
                requirement in new_order for requirement in requirements
            ):
                new_order.append(i)
    return new_order


print(
    sum(
        middle_page(reorder(update, rules))
        for update in updates
        if not valid(update, rules)
    )
)
