n = 5
k = 0

def WhereIdP(k):
    table = []
    ie = 1
    for i in range(k):
        p = ((ie*i)/2)
        ie += 1
        if p > k:
            break   
        table.append(p)

    return len(table)


def create_inverted_list(q):
    table = []
    while True:
        table.append(q)
        q -= 1
        if q <= 0:
            break
        
    return table

def calculated_inv(table_q):
    count = 0
    cal = 0
    for i in table_q:
        cal += 1
        if cal == 1:
            continue
        count += i
    return count
        
def add_count_inv(table_q, total):
    table = []
    for i in table_q:
        if i == total:
            table.append(len(table_q) + 1)
        table.append(i)

    return table

def create_all_table(n, table_q):
    all_count = len(table_q)
    nu = n - all_count
    while True:
        all_count += 1
        if nu <= 0:
            break
        table_q.append(all_count)
        nu -= 1

    return table_q


def main(n, k):
    q = WhereIdP(k)
    table_q = create_inverted_list(q)
    cal = calculated_inv(table_q)
    total = k - cal
    new_table = add_count_inv(table_q, total)
    all_table = create_all_table(n, new_table)
    print(all_table)

main(n, k)
