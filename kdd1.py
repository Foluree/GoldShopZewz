
n = int(input())
count1 = [input() for _ in range(n)]

newst = set(count1)
table = {}
for new in count1:
    table[new] = table.get(new, 0) + 1

freq = []
for i in table:
    freq.append(table[i])

max_freq = max(freq)

names_best = []
for i in table:
    if table[i] == max_freq:
        names_best.append(i)
names_best = sorted(names_best)

print(names_best)

