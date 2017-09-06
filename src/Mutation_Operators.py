import random


def mutation(g_problem, c, prob):
    cm = list(c)  # we make a copy
    for i in range(len(cm)):
        if random.random() < prob:
            cm[i] = random.choice(g_problem.genes)
    return cm


# Pick two allele values at random and move the second to follow the first, shifting the
# rest along to accommodate
def insert_mutation(c1):
    # c1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # c1 = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j']
    # random.shuffle(c1)
    # print c1
    cm = list(c1)
    a = random.randint(0, len(cm) - 2)
    b = random.randint(a + 1, len(cm) - 1)
    cm.insert(a + 1, cm.pop(b))
    return cm


# Pick two alleles at random and swap their positions
def swap_mutation(c1):
    cm = list(c1)
    a = random.randint(0, len(cm) - 2)
    b = random.randint(a + 1, len(cm) - 1)
    cm[b], cm[a] = cm[a], cm[b]
    return cm


# Pick two alleles at random and then invert the substring between them
def inverse_mutation(c1):
    cm = list(c1)
    a = random.randint(0, len(cm) - 2)
    b = random.randint(a + 1, len(cm) - 1)

    cm[a:b + 1] = cm[a:b + 1][::-1]
    return cm
