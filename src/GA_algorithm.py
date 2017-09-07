import random
import Utils
import time
import Crossover_Operators as cr_op
import Mutation_Operators as mu_op

""" Lo que sigue es un esquema general de un algoritmo genético:

1.Inicializar la población.
2.Evaluar cada individuo de la población.
3.Repetir hasta Condición de Terminación:
    -Seleccionar padres.
    -Cruzar pares de padres.
    -Mutar los hijos resultantes.
    -Evaluar los nuevos individuos
    -Seleccionar los individuos para formar la siguiente generación.
4.Devolver el mejor individuo de la última generación. """


class Problem_Genetic():
    """ Class to represent problems to be solved by means of a general
    genetic algorithm. It includes the following attributes:
    - genes: list of possible genes in a chromosome
    - individuals_length: length of each chromosome
    - decode: method that receives the genotype (chromosome) as input and returns
       the phenotype (solution to the original problem represented by the chromosome)
    - fitness: method that returns the evaluation of a chromosome (acts over the
       genotype)
    - mutation: function that implements a mutation over a chromosome
    - crossover: function that implements the crossover operator over two chromosomes"""

    def __init__(self, genes, decode, crossover, mutation, start_point):
        self.genes = genes
        self.decode = decode
        self.mutation = mutation
        self.crossover = crossover
        self.start_point = start_point
        self.individual_length = len(genes)

    def mutation(self, c, prob):
        cm = list(c)  # we make a copy
        for i in range(len(cm)):
            if random.random() < prob:
                cm[i] = random.choice(c)
        return cm


def fitness(prob_g, gen):
    # check min path and penalize if it doesnt begin and finish in start_point
    gen_aux = list(gen)
    gen_aux.insert(0, prob_g.start_point)
    gen_aux.insert(len(gen_aux), prob_g.start_point)
    distance = 0
    for i, g1 in enumerate(gen_aux[1:]):
        distance += Utils.haversine(g1, gen_aux[i])
    return distance if (gen_aux[0] is prob_g.start_point and gen_aux[-1] is prob_g.start_point and len(gen) == len(
        set(gen))) else distance * 1000000000


def initial_population(prob_g, size):
    return [random.sample(prob_g.genes, len(prob_g.genes)) for _ in range(size)]


def crossover_parents(prob_g, parents):
    kids = []
    if prob_g.crossover == 1:
        for j in range(0, len(parents)):
            a, b = random.sample(parents, 2)
            kids.append(cr_op.crossover(prob_g, a, b))
        return kids

    elif prob_g.crossover == 2:
        for j in range(0, len(parents)):
            a, b = random.sample(parents, 2)
            kids.append(cr_op.order_crossover(a, b))
            kids.append(cr_op.order_crossover(b, a))
        return kids
    else:
        for j in range(0, len(parents)):
            a, b = random.sample(parents, 2)
            kids.append(cr_op.edge_crossover(a, b))
            kids.append(cr_op.edge_crossover(b, a))
        return kids


def crossover_parents_cellular_genetic(prob_g, parents):
    kids = []
    if prob_g.crossover == 1:
        for j in range(0, len(parents), 2):
            a = parents[j]
            b = parents[j + 1]
            kids.append(cr_op.crossover(prob_g, a, b))
        return kids

    elif prob_g.crossover == 2:
        for j in range(0, len(parents), 2):
            a = parents[j]
            b = parents[j + 1]
            kids.append(cr_op.order_crossover(a, b))
            kids.append(cr_op.order_crossover(b, a))
        return kids
    else:
        for j in range(0, len(parents), 2):
            a = parents[j]
            b = parents[j + 1]
            kids.append(cr_op.edge_crossover(a, b))
            kids.append(cr_op.edge_crossover(b, a))

        return kids


def mutate_individuals(prob_g, population, prob):
    sol = []
    if prob_g.mutation == 1:
        for j in range(0, len(population)):
            sol.extend(mu_op.mutation(prob_g, population[j], prob))
    elif prob_g.mutation == 2:
        for j in range(0, len(population)):
            if random.random() < prob:
                sol.extend([mu_op.insert_mutation(population[j])])
            else:
                sol.extend([population[j]])
    elif prob_g.mutation == 3:
        for j in range(0, len(population)):
            if random.random() < prob:
                sol.append(mu_op.swap_mutation(population[j]))
            else:
                sol.append(population[j])
    else:
        for j in range(0, len(population)):
            if random.random() < prob:
                sol.append(mu_op.inverse_mutation(population[j]))
            else:
                sol.append(population[j])
    return sol


def select_one_tournament(problem_genetic, population, k, opt):
    participants = random.sample(population, k)
    return opt(participants, key=lambda x: (fitness(problem_genetic, x)))


def tournament_selection(problem_genetic, population, n, k, opt):
    return [select_one_tournament(problem_genetic, population, k, opt)
            for _ in range(n)]


def new_generation(problem_genetic, opt, population, n_parents, n_direct, prob_mutate, cellular):
    k = 3
    parents = tournament_selection(problem_genetic, population, n_parents, k, opt)
    if cellular:
        kids = crossover_parents_cellular_genetic(problem_genetic, parents)
    else:
        kids = crossover_parents(problem_genetic, parents)
    direct_surv = tournament_selection(problem_genetic, population, n_direct, k, opt)
    sol = mutate_individuals(problem_genetic, kids + direct_surv, prob_mutate)
    return sol


# genetic_algorithm_t(sq_gen,3,min,20,10,0.7,0.1)
def genetic_algorithm_main(problem_genetic, ngen, size, ratio_cross, prob_mutate, opt, cellular):
    start = time.time()
    population = initial_population(problem_genetic, size)
    n_parents = round(size * float(ratio_cross))
    n_parents = (n_parents if n_parents % 2 == 0 else n_parents - 1)
    n_direct = size - n_parents

    for _ in range(ngen):  # halting condition, number of iterations
        population = new_generation(problem_genetic, opt, population, n_parents, n_direct, float(prob_mutate), cellular)

    best_chr = opt(population, key=lambda x: (fitness(problem_genetic, x)))
    best_distance = fitness(problem_genetic, best_chr)
    best_chr.insert(0, problem_genetic.start_point)
    best_chr.insert(len(best_chr), problem_genetic.start_point)
    end = time.time()
    total_time = end - start
    print([str(i) + "-" + str(city) for i, city in enumerate(best_chr)], ', ' + str(best_distance) + ' km', total_time)
    Utils.print_map(best_chr)
