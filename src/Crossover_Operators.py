'''
Genes = [1-9]
individuals_length = genes +1 the journey stars and ends at the same point
Chromosome [1,2,3,4,5,6,7,8,9,1]
'''

import random


def crossover(g_problem, c1, c2):
    pos = random.randrange(1, g_problem.individuals_length - 1)
    cr1 = c1[:pos] + c2[pos:]
    cr2 = c2[:pos] + c1[pos:]
    return [cr1, cr2]


def pmx_crossover(c1, c2):
    pass


def order_crossover(c1, c2):
    # c1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # c2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
    # print 'c2', c2
    # random.shuffle(c1)
    a = random.randint(0, len(c1) - 2)  # get two random index a < b
    b = random.randint(a + 1, len(c1) - 1)

    # lets create a list with the same length of c1 and c2
    # and fill it with zeros
    r = [0] * len(c1)
    # copy the random sublist of c1 at same position in the list r
    r[a:b + 1] = c1[a:b + 1]
    # print 'a: ', a, 'b: ', b
    # print 'c1: ', c1
    # print 'r:  ', r

    r1 = c2[b + 1:] + c2[:b + 1]  # get the elements from c2 in order
    # print 'c2: ', c2
    # print 'r1: ', r1
    r1 = [x for x in r1 if x not in r]  # filter the elements to get only the elements that are not in r
    # print 'r1:', r1
    r[b + 1:], r[:a] = r1[:len(r) - 1 - b:], r1[len(r) - 1 - b:]
    # print r
    return r


def counter_choices(elements):
    # this method is created simulate if an edge is common to both list and is marked with a +
    # choices example [5, 2, 5, 3]
    # function result = [[2,3,5][2]] [[all choices][repeated choices]]
    choices = set()
    repeated = set()
    for choice in elements:
        if choice in choices:
            repeated.add(choice)
        else:
            choices.add(choice)
    return [choices, repeated]


def edge_crossover_table(c1, c2):
    table = {}
    # c1 = range(1, 10)
    # c2 = range(1, 10)
    # random.shuffle(c1), random.shuffle(c2)

    for i in range(0, len(c1)):
        element = c1[i]
        element2 = c2.index(element)  # position of element1 in c2
        if i == len(c1) - 1:  # check if we are at the last position of c1
            if element2 == len(c1) - 1:  # check if we are at the last position of c2
                table[element] = counter_choices([c1[len(c1) - 2], c1[0], c2[element2 - 1], c2[0]])
            else:
                table[element] = counter_choices([c1[len(c1) - 2], c1[0], c2[element2 - 1], c2[element2 + 1]])
        else:
            if element2 == len(c1) - 1:
                table[element] = counter_choices([c1[i - 1], c1[i + 1], c2[element2 - 1], c2[0]])

            else:
                table[element] = counter_choices([c1[i - 1], c1[i + 1], c2[element2 - 1], c2[element2 + 1]])

    return table


def delete_current_from_table(table, current):
    table.pop(current, None)
    for a in table.values():
        a[0].discard(current)
        a[1].discard(current)
    return table


def edge_crossover():
    # c1 = range(1, 10)
    # c2 = range(1, 10)
    # random.shuffle(c1), random.shuffle(c2)
    c1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    c2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
    print 'c1:', c1
    print 'c2:', c2
    table = edge_crossover_table(c1, c2)
    print 'table: ', table

    element = random.randint(1, len(table.keys()))
    offspring = [element]
    choices = table[element]
    table = delete_current_from_table(table, element)
    print 'table: ', table

    while table.keys():
        if choices[1]:
            element = list(choices[1])[0]
        else:
            helper = [(key, len(table[key][0])) for key in choices[0]]
            helper.sort(key=lambda x: x[1])
            element = helper[0][0]

        choices = table[element]
        table = delete_current_from_table(table, element)
        offspring.append(element)
        print table
    print 'offspring: ', offspring


edge_crossover()
