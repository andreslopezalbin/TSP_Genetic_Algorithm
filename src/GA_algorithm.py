import random

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

    def __init__(self, genes, individuals_length, decode, fitness):
        self.genes = genes
        self.individuals_length = individuals_length
        self.decode = decode
        self.fitness = fitness


