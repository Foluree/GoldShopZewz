field = 1
moves = 1
tiles = [1]

def create_table(count):
    main_table = []
    for i in range(count):
        table = []
        for ie in range(count):
            table.append(0)

        main_table.append(table)

    return main_table

def print_table(main_table):
    for i in main_table:
        print(i)

def calculatet_pozition(count, filed):
    x = 0
    y = 0
    while True:
        #print(x, y, count)
        if (count - filed) <= 0:
            y = count
            y -= 1
            break
        count -= filed    
        x += 1
    return x, y

def check_goziontal_line(main_table, field):
    for i in main_table:
        cal = 0
        for ie in i:
            if ie == 1:
                cal+=1
            if cal == field:
                #print("Yes")
                return True
    return False

def check_vertival_line(main_table, field):
    
    cut = field
    #print(field)
    while True:

        #print(cut)
        if cut == 0:
            break
        cut -= 1
        cute = field
        cal = 0

        while True:
            if cute == 0:
                break
            cute -= 1
            #print(cute, cut, "cute", cal)
            if main_table[cute][cut] == 1:
                cal += 1
                if cal == field:
                    return True
    return False

def check_dioganal(main_table, field):
    x = 0
    y = 0
    x1 = 0
    y1 = (field - 1)
    cuz = 0
    cuz1 = 0
    while True:
        if main_table[x][y] == 1:
            cuz += 1
            if cuz == field:
                return True
        if main_table[x1][y1] == 1:
            cuz1 += 1
            if cuz1 == field:
                return True

        if y1 == 0:
            break

        x += 1
        y += 1
        x1 += 1
        y1 -= 1
        
    return False


def check_tables(main_table, field):
    if check_vertival_line(main_table, field):
        return True
    elif check_goziontal_line(main_table, field):
        return True
    elif check_dioganal(main_table, field):
        return True
    else:
        return False



#print(poz, x, y)
def main_calculated(tiles, field):
    main_table = create_table(field)
    count = 0
    for i in tiles:
        x, y = calculatet_pozition(i, field)
        main_table[x][y] = 1
        count += 1
        print_table(main_table)
        print('')
        if check_tables(main_table, field):
            return count
    return -1



wins = main_calculated(tiles, field)
print(wins)