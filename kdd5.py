n = 5
q = 3

initial_edge = [
    (1, 2, 2),
    (2, 3, 3),
    (3, 4, 4),
    (4, 5, 5)
]  # дерево-путь, сумма = 14

queriers = [
    (1, 5, 1),
    (1, 3, 2),
    (2, 5, 3)
]

def create_ideal(ideal_table, i):
    ideal_table2 = []
    count = len(ideal_table) 
    cal = 0
    for ie in ideal_table:


        if ie[0] == i[0] and ie[1] == i[1]:

            if ie[2] > i[2]:


                ideal_table2.append(i)

                continue

            else:
                
                ideal_table2.append(ie)
                continue

        else:
            cal += 1
            ideal_table2.append(ie)
            continue

    if cal == count:
        ideal_table2.append(i)

    return ideal_table2
        

def coll_ideal(ideal_table, n):
    ideal_table0 = ideal_table.copy()
    nq = (n - 1)
    table = []
    while True:
        count = 0
        count1 = 0
        dele = 0

        if nq == 0:
            break

        for i in ideal_table0:
            #print(i)
            if count1 == 0:
                count = i[2]
            count1 += 1
            if i[2] <= count:
                dele = count1
                count = i[2]
        
        table.append(count)
        dele -= 1
        nq -= 1
        #print(dele)
        #print(ideal_table0)
        ideal_table0.pop(dele)

    return table


def cal_ideal(coll):
    count = 0
    for i in coll:
        count += i
    return count



def search_element(ideal_table, search):
    search = search.copy()
    black_list = create_black_list(search)
    #print(black_list, "black_list, in search", search, "to_search ->", search[0][-1][1], '-> len search', len(search))
    if len(search) == 1:
        #print("yes one search", search[0][-1][1], )
        search_to = search[0][-1][1]
    #else:
    #    print("yes two search", search[-1][1], '|' , search[-1],)
    #    search_to = search[-1][1]
    table = []
    for iu in ideal_table:

        if search_to == iu[0]:
            #print(iu[0], "two count", iu[1] , "<-|->", black_list, "test_black_list")
            if not iu[0] in black_list:
                if not iu[1] in black_list:
                    #print("added iu[0] and iu[1]", iu[0], "<-|->", iu[1])
                    table.append(iu)
                else:
                    continue
            else:
                continue
        else:
            continue

    #print()

    if len(table) == 0:
        return []
    elif len(table) == 1:
        sur = search[0].copy()
        sur.extend(table)
        #print(search, table)
        #search.extend(table)
        #print(sur, "search_len 1", len(search))
        return [sur]
    elif len(table) > 1:
        big_table = []
        #print(search , "<-|->" ,table, "elif search table")
        for i in table:
            sur = search[0].copy()
            #print(sur, i, "elif search 1 table")
            sur.append(i)
            big_table.append(sur)

        return big_table

def append_table():
    pass


def create_black_list(table):
    black_list = []

    #print(table, "in black list start", )

    try:
        if len(table) == 1:
            tablo = table[0]
            for i in tablo:
                #print(i, "Black lis for")
                black_list.append(i[0])
    except:
        #print(table, "in black list")
        black_list.append(table[0][0])

    #print(black_list, "black_list")

    return black_list



def create_facets_woods(ideal_table, n):

    all_woods = []
    nu = n - 1
    ideal_table1 = ideal_table.copy()
    for i in ideal_table1:

        small_table = []
        request = []
        small_table.append(i)
        request.append(small_table)
        #print("With start", request, "-->", small_table)
        #print(all_woods, "all_woods")
        while True:

            if not len(request) == 0:
                if len(request) == 1:
                    request = search_element(ideal_table, request)
                    #print(request, "yes 1 accept request")
                if len(request) > 1:
                    request1 = request.pop(0)
                    #print(request1, "request1", len(request1))
                    the_request = search_element(ideal_table, [request1])
                    if len(the_request) != 0:
                        request.extend(the_request)
                        #print(request, "yes accept request")

            else:
                break

            if len(request) > 1:
                new_request = []
                for i in request:
                    if len(i) == nu:
                        all_woods.append(i)
                    else:
                        new_request.append(i)
                request = new_request

            if len(request) == 1:
                if len(request[0]) == nu:
                    all_woods.append(request[0])
                    break


    return all_woods

def cal_all(all_woods):
    best_count = 0
    best_result = 0
    count1 = 0
    for i in all_woods:
        count = 0
        for iu in i:
            count += iu[2]

        if count1 == 0:
            best_count = count
            count1+=1

        if count <= best_count:
            #print(best_count, "best_count", best_result)
            best_count = count
            best_result = i

    print(best_count, best_result)

#def create_all_woods(table):
#    for i in table:


def create_tree(ideal_table, n):
    trees = []
    length = n - 1

    def build(tree, nodes, start):
        if len(tree) == length:
            trees.append(tree.copy())
            return

        for edge in ideal_table:
            print(edge)
            a, b, w = edge

            if edge in tree:
                continue

            if a in nodes or b in nodes:
                if a not in nodes or b not in nodes:
                    tree.append(edge)
                    build(tree, nodes | {a, b}, start)
                    tree.pop()

    for edge in ideal_table:
        build([edge], {edge[0], edge[1]}, edge[0])

    return trees

        
def main():
    ideal_table = initial_edge
    for i in queriers:

        ideal_table = create_ideal(ideal_table, i)
        #create_all_woods(ideal_table)

        #@all_woods = create_facets_woods(ideal_table, n)
        all_woods = create_tree(ideal_table, n)
        #coll = coll_ideal(ideal_table, n)
        #cal = cal_ideal(coll)
        #print(all_woods)
        cal_all(all_woods)

main()