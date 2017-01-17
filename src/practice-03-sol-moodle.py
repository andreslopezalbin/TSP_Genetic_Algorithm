# practice-03.py
# Inteligencia Artificial, tercer curso del Grado de Ingeniería Informática -
# Grupo en Inglés. Universidad de Sevilla.

# Practice 3: Genetic algorithms
# ===========================================================================

# On this practice we will work with a Python implementation of a
# genetic algorithm. We will also study several particular instances
# of the Knapsack problem.
# The practice consists on three parts:

# * Part I: Implementation of a specific genetic algorithm.
# * Part II: Implementation of the representation of the Knapsack
#    problem in the genetic algorithms framework.
# * Part III: Experimentation using the defined instances.

# We will need again the random module (as in practice-02)
import random


# ==============================================
# Part I: Implementation of a genetic algorithm 
# ==============================================

# -----------
# Exercise 1
# -----------

# Implement the class Problem_Genetic gathering the necessary elements
# of the representation of optimization problems to be solved by a
# genetic algorithm. More precisely, these elements are:

# - genes: list of the genes used in the genotype of the individuals
# - individuals_length: length of the chromosomes
# - decode: function that transforms the genotype into the phenotype
# - fitness: function that evaluates the individuals, to be optimized
#   

# All these data and functions will be stored on the corresponding
# data attributes of the class.

# Besides, the class should include two methods:
# - mutation: mutates a chromosome 
# - crossover: given a pair of chromosomes performs crossover on them
# Implement the mutations and crossover as explained in slides of unit-04.

# Please notice that in the definition of this class we do not specify
# whether it is a maximization or a minimization problem. This will be
# set by means of an input parameter for the genetic algorithm that we
# are going to implement. 

# ================ Solution:


class Problem_Genetic(object):
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

    def __init__(self, genes, individuals_length, decode, fitness):
        self.genes = genes
        self.individuals_length = individuals_length
        self.decode = decode
        self.fitness = fitness

    def mutation(self, c, prob):
        cm = list(c)  # we make a copy
        for i in range(len(cm)):
            if random.random() < prob:
                cm[i] = random.choice(self.genes)
        return cm

    def crossover(self, c1, c2):
        pos = random.randrange(1, self.individuals_length - 1)
        cr1 = c1[:pos] + c2[pos:]
        cr2 = c2[:pos] + c1[pos:]
        return [cr1, cr2]


# ==================


# -----------
# Exercise 2
# -----------

# Define a variable sq_gen, storing an instance of the previous class,
# corresponding to the problem of optimizing (maximize or minimize)
# the square function over the set of natural numbers smaller than 2^{10}.

# The following function that interprets a list of 0s and 1s as a
# natural number will be useful:  

def binary_to_decimal(x):
    return sum(b * (2 ** i) for (i, b) in enumerate(x))


# After defining sq_gen, test some of the functions defined in the
# previous class, on this particular instance. For example:

# >>> sq_gen.decode([1,0,0,0,1,1,0,0,1,0,1])
# 1329
# >>> sq_gen.fitness([1,0,0,0,1,1,0,0,1,0,1])
# 1766241
# >>> sq_gen.mutation([1,0,0,0,1,1,0,0,1,0,1],0.1)
# [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
# >>> sq_gen.mutation([1,0,0,0,1,1,0,0,1,0,1],0.1)
# [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
# >>> sq_gen.crossover([1,0,0,0,1,1,0,0,1,0,1],[0,1,1,0,1,0,0,1,1,1])
# [[1, 0, 0, 0, 1, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1]]



# ============= Solution:

def fit_sq(x):
    return (binary_to_decimal(x)) ** 2


sq_gen = Problem_Genetic([0, 1], 10, binary_to_decimal, fit_sq)

#genes, individuals_length, decode, fitness
# sq_gen = Problem_Genetic([0,1], 10, binary_to_decimal,
#                          lambda x: (binary_to_decimal(x))**2 )


# ==========================


# -----------
# Exercise 3
# -----------

# Define a function initial_population(problem_genetic,size), that
# creates an initial population of a given size, for an instance
# of the previous class Problem_Genetic

# HINT: Use random.choice

# ======== Solution:

def initial_population(problem_genetic, size):
    return [[random.choice(problem_genetic.genes)
             for _ in range(problem_genetic.individual_length)]
            for _ in range(size)]


# =========================

# -----------
# Exercise 4
# -----------

# Define a function crossover_parents(problem_genetic,parents), that
# receives an instance of Problem_Genetic and a population of parents,
# and returns the new population obtained by performing the crossover
# operation pairwise (parents are coupled as they appear on the list).

# ======= Solution

def crossover_parents(prob_g, parents):
    kids = []
    for j in range(0, len(parents), 2):
        kids.extend(prob_g.crossover(*parents[j:j + 2]))
    return kids


# ================



# -----------
# Exercise 5
# -----------

# Define a function
# mutate_individuals(problem_genetic, population, prob), that given an
# instance of Problem_Genetic, a population and a probability of
# mutation, returns the population obtained after applying (with
# probability p) mutations over the genes of the individuals of the
# population.

# =========== Solution:


def mutate_individuals(problem_genetic, population, prob):
    sol = []
    for j in range(0, len(population)):
        sol.extend(problem_genetic.mutation(population[j], prob))
    return sol

    # return list(map(lambda x: problem_genetic.mutation(x,prob), population))


# =============================================


# -----------
# Exercise 6
# -----------

# Define a function
# tournament_selection(problem_genetic,population,n,k,opt) that
# implements the selection by tournament of n individuals of a
# population.  The function receives as input: an instance of
# Problem_Genetic, a population, a natural number n (number of
# individuals to be selected), a natural number k (number of
# participants in the tournament), and a function opt that can be
# either function max or function min (indicating if it is a
# maximization or a minimization problem).

# HINT: Use random.sample 

# ======= Solution:

def select_one_tournament(problem_genetic, population, k, opt):
    participants = random.sample(population, k)
    return opt(participants, key=problem_genetic.fitness)


def tournament_selection(problem_genetic, population, n, k, opt):
    return [select_one_tournament(problem_genetic, population, k, opt)
            for _ in range(n)]


# ================




# -----------------------------

# The following function genetic_algorithm_t implements a
# genetic algorithm using tournament selection.


def genetic_algorithm_t(problem_genetic, k, opt, ngen, size, ratio_cross, prob_mutate):
    population = initial_population(problem_genetic, size)
    n_parents = round(size * ratio_cross)
    n_parents = (n_parents if n_parents % 2 == 0 else n_parents - 1)
    n_direct = size - n_parents

    for _ in range(ngen):
        population = new_generation_t(problem_genetic, k, opt, population, n_parents, n_direct, prob_mutate)

    best_chr = opt(population, key=problem_genetic.fitness)
    best = problem_genetic.decode(best_chr)
    return (best, problem_genetic.fitness(best_chr))


# The function receives as input:

# * problem_genetic: an instance of the class Problem_Genetic, with
#     the optimization problem that we want to solve.
# * k: number of participants on the selection tournaments.
# * opt: max or min, indicating if it is a maximization or a
#     minimization problem.
# * ngen: number of generations (halting condition)
# * size: number of individuals for each generation
# * ratio_cross: portion of the population which will be obtained by
#     means of crossovers. 
# * prob_mutate: probability that a gene mutation will take place.


# -----------
# Exercise 7
# -----------

# Define the auxiliary function left undefined in the previous
# algorithm; that is, function
# new_generation_t(problem_genetic,k,opt,population,n_parents,n_direct,prob_mutate)
# that given a population, returns a new one (the next generation).

# After defining it, run the previous genetic algorithm to solve the
# sq_gen problem (both in its minimization and maximization variants).

# For example:

# >>> genetic_algorithm_t(sq_gen,3,min,20,10,0.7,0.1)
# (0, 0)
# >>> genetic_algorithm_t(sq_gen,3,max,20,10,0.7,0.1)
# (1023, 1046529)

# NOTE: recall that the output of genetic_algorithm_t is a pair with
# the best phenotype found, and its fitness (objective function value).


# =========== Solution:

def new_generation_t(problem_genetic, k, opt, population, n_parents, n_direct, prob_mutate):
    parents = tournament_selection(problem_genetic, population, n_parents, k, opt)
    kids = crossover_parents(problem_genetic, parents)
    direct_surv = tournament_selection(problem_genetic, population, n_direct, k, opt)
    sol = mutate_individuals(problem_genetic, kids + direct_surv, prob_mutate)
    return sol


# =======================



# ================================================
# Part II: Representation of the Knapsack problem
# ================================================


# The Knapsack problem can be stated as follows: given n objects of
# weights w_i and value v_i (i=1,...,n), select which objects should
# be carried in a knapsack having a maximum weight P, in such a way
# that the value of the selected objects is maximum.

# We will use the following representation:
# GENES: [0,1]
# INDIVIDUALS-LENGTH: N
# DECODE(X): we read the chromosome from left to right, a 1 at
#    position i means that the i-th object is selected, with the
#    following exception:
#    If by selecting the object we go beyond the max weight, then this
#    object is not selected (and neither is none of the remaining).
# F-OBJECTIVE(X): sum of the values of the selected objects
#    (note that no penalty is required because of our decode function)


# -----------
# Exercise 8
# -----------

# Define a function 
# decode_knapsack(chromosome, n_objects, weights, capacity)
# that receives as input:

# - a chromosome (i.e. a list of 0s and 1s, of length equal to
#     n_objects) 
# - n_objects: total number of available objects
# - weights: a list with the weight of each object
# - capacity: maximum weight of the knapsack.

# The output of this function is a list of 0s and 1s representing the
# set of selected objects (the i-th object is selected if and only if
# there is a 1 at position i). This list is obtained from the
# chromosome, filtering the objects that are discarded according to
# the DECODE description.


# ========== Solution:






# ==============================================


# -----------
# Exercise 9
# -----------

# Define a function 

# fitness_knapsack(chromosome, n_objects, weights, capacity, values)

# that calculates the total value of the objects carried out inside the knapsack
# represented by the chromosome, according to the codification
# explained in the previous exercise.
# The function receives as input the same arguments as the previous
# function, together with 'values', which is a list with the value of
# each object.


# ============== Solution:





# ===============================================



# =====================================================
# Part III: Solving instances of the  Knapsack problem
# =====================================================


# Below you can find three particular instances of the Knapsack
# problem. Their corresponding optimal solutions are also given, in
# order to compare them against the results obtained by the genetic
# algorithm:

# _______________________________________________________
# Knapsack problem 1:
# 10 objects, maximum weight 165
weights1 = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
values1 = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

# Optimal solution= [1,1,1,1,0,1,0,0,0,0], value= 309
# _______________________________________________________

# _______________________________________________________
# Knapsack problem 2:
# 15 objects, maximum weight 750

weights2 = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
values2 = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]

# Optimal solution= [1,0,1,0,1,0,1,1,1,0,0,0,0,1,1], value= 1458
# _______________________________________________________


# _______________________________________________________
# Knapsack problem 3:
# 24 objects, maximum weight 6404180
weights3 = [382745, 799601, 909247, 729069, 467902, 44328,
            34610, 698150, 823460, 903959, 853665, 551830, 610856,
            670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]
values3 = [825594, 1677009, 1676628, 1523970, 943972, 97426,
           69666, 1296457, 1679693, 1902996,
           1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367,
           853655, 1826027, 65731, 901489, 577243, 466257, 369261]

# Optimal solution= [1,1,0,1,1,1,0,0,0,1,1,0,1,0,0,1,0,0,0,0,0,1,1,1], value= 13549094

# _______________________________________________________


# -----------
# Exercise 10
# -----------

# Define variables k1g, k2g and k3g, containing the instances of
# Problem_Genetic corresponding, respectively, to the previous three
# instances of the knapsack problem.

# Use the genetic algorithm to solve these problems.

# For example:

# >>> genetic_algorithm_t(k1g,3,max,100,50,0.8,0.05)
# ([1, 1, 1, 1, 0, 1, 0, 0, 0, 0], 309)

# >>> genetic_algorithm_t(k2g,3,max,100,50,0.8,0.05)
# ([1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0], 1444)
# >>> genetic_algorithm_t(k2g,3,max,200,100,0.8,0.05)
# ([0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0], 1439)
# >>> genetic_algorithm_t(k2g,3,max,200,100,0.8,0.05)
# ([1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1], 1458)

# >>> genetic_algorithm_t(k3g,5,max,400,200,0.75,0.1)
# ([1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0], 13518963)
# >>> genetic_algorithm_t(k3g,4,max,600,200,0.75,0.1)
# ([1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], 13524340)
# >>> genetic_algorithm_t(k3g,4,max,1000,200,0.75,0.1)
# ([1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], 13449995)
# >>> genetic_algorithm_t(k3g,3,max,1000,100,0.75,0.1)
# ([1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], 13412953)
# >>> genetic_algorithm_t(k3g,3,max,2000,100,0.75,0.1)
# ([0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 13366296)
# >>> genetic_algorithm_t(k3g,6,max,2000,100,0.75,0.1)
# ([1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1], 13549094)



# =========== Solution:






# ===================================

# End of file
