with open("01/input.txt") as file:
    pairs = [line.split() for line in file]


l_list = sorted([int(pair[0]) for pair in pairs])
r_list = sorted([int(pair[1]) for pair in pairs])

# part 1
print(sum(abs(l - r) for l, r in zip(l_list, r_list)))

# part 2
counts = {}
for i in r_list:
    if i in counts:
        counts[i] += 1
    else:
        counts[i] = 1

print(sum(i * counts.get(i, 0) for i in l_list))
