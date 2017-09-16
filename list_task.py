def remove_adjacent(lst):
    return list(set(lst))


def linear_merge(lst1, lst2):
    i = 0
    j = 0
    lst = []
    while i < len(lst1) or j < len(lst2):
        if i == len(lst1):
            lst.append(lst2[j])
            j += 1
        elif j == len(lst2):
            lst.append(lst1[i])
            i += 1
        elif lst1[i] < lst2[j]:
            lst.append(lst1[i])
            i += 1
        else:
            lst.append(lst2[j])
            j += 1
    return lst