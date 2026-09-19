from itertools import product

n = 3    #количесво раундов
prizes = [
    [7, 1, 4], # устаник 1
    [7, 3, 5], # участик 2
    [2, 8, 6], # устаник 3
    [8, 6, 3], # устаник 4
    [10, 9, 6], #5
    [4, 5, 7], #6
    [3, 10, 9], # 7
    [4, 3, 5] # 8
] #призовые

total_playes = 8 #игроки

def create_all_var(n):
    m = 1 << n
    players = list(range(1, m + 1))

    variants = [([], players)]

    for round_num in range(1, n + 1): #round_num
        new_variants = []
        for history, current in variants:
            num_paris = len(current) // 2
            pair_choices = list(product([0, 1], repeat=num_paris))
            for choices in pair_choices:
                winners = []
                round_paris = []
                for idx, choice in enumerate(choices):
                    a = current[2 * idx]
                    b = current[2 * idx + 1]
                    if choice == 0:
                        winner, loser = a, b
                    else:
                        winner, loser = b, a
                    winners.append(winner)
                    round_paris.append((winner, loser))
                new_history = history + [round_paris]
                new_variants.append((new_history, winners))

        variants = new_variants

    return variants

def create_table(n):
    table = []
    tu = create_all_var(n)
    for i in tu:
        table.append([i[0][1:], i[1]])
    return table

def deep_recursev(table):
    table2 = []
    for i in table:
        result = list(reversed(i[0] + i[1]))
        table2.append(result)
    return table2

def deep_recursev1(table):
    table2 = []
    for i in table:
        count = len(i)
        table1 = []
        iu = i
        #print(iu)
        for ie in i:
            print(count - 1, iu[count - 1], ie)
            table1.append(iu[count - 1])
            count -= 1
        table2.append(table1)

    return table2        
    


table = create_table(n)
#table1 = deep_recursev(table)
#table1 = deep_recursev(table)
#print(table)

def transform(data):
    def unwrap_single_list(x):
        while isinstance(x, list) and len(x) == 1 and isinstance(x[0], list):
            x = x[0]
        return x

    number = None
    levels = None

    for item in data:
        if isinstance(item, list):
            if len(item) == 1 and isinstance(item[0], (int, float)):
                number = item[0]
            else:
                levels = item

    if number is None or levels is None:
        raise ValueError("No search")

    levels = unwrap_single_list(levels)

    return [[number]] + levels[::-1]

def remove_first_values(data):
    result = []

    for level in data:
        # Первый элемент — число, его оставляем
        if len(result) == 0:
            result.append(level)
            continue

        # Если уровень содержит пары (x, y)
        new_level = []

        for item in level:
            if isinstance(item, tuple) and len(item) >= 2:
                new_level.append(item[1])
            else:
                new_level.append(item)

        result.append(new_level)

    return result

def create_id_table(table):
    table2 = []
    for i in table:
        tabl = transform(i)
        tablo = remove_first_values(tabl)
        table2.append(tablo)
        #print(tablo)
    return table2

table = create_id_table(table)

#for i in table:
#    print(i)


def create_tebe_1(table):
    total_table = []
    count = -1
    for ie in table:
        table2 = []
        count += 1
        print(ie, count)
        for iu in ie:
            tablu = []
            if len(iu) > 1:
                for io in iu:
                    ime = io
                    print(ime)
                    im = ime - 1
                    tablu.append(im)
                #new = (tablu)
            if len(iu) == 1:
                im = iu[0] - 1
                new = im

            table2.append(new)

        total_table.append(table2)

    return total_table


def recursive(data):
    if isinstance(data, list):
        return [recursive(item) for item in data]

    return data

#table = create_tebe_1(table)
#table = recursive(table)
#print(table)




def cal():
    total_count = 0
    best_game = 0

    for i in table:
        ne = n
        count = 0
        count_be = 0
        for iu in i:
            ne = ne - 1
            if len(iu) > 1:
                for io in iu:
                    ime = io - 1
                    counts = prizes[ime][ne]
                    count += counts
            if len(iu) == 1:
                #print(iu, ne)
                im = iu[0] - 1
                count = prizes[im][ne]
            count_be += count
        if count_be >= total_count:
            total_count = count_be
            best_game = i

    print(total_count, best_game)

cal()
#print(total_count, best_game)
        

        


"""
напиши python скрипт который бы разберал[[[(4, 2), (8, 6), (12, 10), (16, 14)], [(8, 4), (16, 12)], [(16, 8)]], [16]]] на это [[16], [(16, 8)], [(8, 4), (16, 12)], [(4, 2), (8, 6), (12, 10), (16, 14)]] или так из этого [[[(4, 2), (8, 6)], [(8, 4)]], [8]] в это [[8], [(8, 4)], [(4, 2), (8, 6)]] так же сдесь есть лишне []
"""

