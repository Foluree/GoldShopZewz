n = 6
k = 3
list1 = [1, 2, 3, 4, 5, 6]

def create_var(list1):
    set1 = []
    #print(len(list1))
    for i in range(len(list1)):
        for iu in range(len(list1)):
            if i <= iu:
                added = (i, iu)
                if not added in set1:
                    set1.append((added))
    return set1


set1 = create_var(list1)

#print(set1)


def create_points(set1):
    all_table = []
    for i in set1:
        a , b = i
        table = []
        #a = a - 1
        b = b + 1

        #print(a, b, "print")
        for i in range(a, b):
            #if i in list1:
            table.append(i)
        all_table.append(table)
    return all_table


#all_table = create_points(set1)
#print(all_table)

def counts_cal(all_table):
    big_table = []
    for i in all_table:

        table = 0
        
        for iu in i:

            #print(iu)
            table += list1[iu]

        big_table.append((table))#, i))

    return big_table

#big_table = counts_cal(all_table)

#print(big_table)

def last_cal(big_table, k):

    last_table = []

    for i in big_table:

        iu = i#[0]

        ku = iu / k


        if ku.is_integer():
            #print(ku)
            last_table.append(i)

    return len(last_table)


def main(n, k, list1):
    set1 = create_var(list1)
    all_table = create_points(set1)
    big_table = counts_cal(all_table)
    last_table = last_cal(big_table, k)

    print(last_table)

main(n, k, list1)