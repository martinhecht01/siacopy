import math
import random

from src.crossover.CrossoverABC import CrossoverABC
from src.classes.Genotype import Genotype


class Annular(CrossoverABC):
    @classmethod
    def cross(cls, gene1: Genotype, gene2: Genotype) -> tuple[Genotype, Genotype]:
        gene1_arr = gene1.to_array()
        gene2_arr = gene2.to_array()

        gene_count = len(gene1_arr)
        last_gene_index = gene_count - 1

        point = random.randrange(0, last_gene_index)
        length = random.randrange(0, math.ceil(last_gene_index / 2))

        child1 = gene1_arr.copy()
        child2 = gene2_arr.copy()

        for i in range(point, point + length):
            child1[i % gene_count] = gene2_arr[i % gene_count]

        for i in range(point, point + length):
            child2[i % gene_count] = gene1_arr[i % gene_count]

        return Genotype.from_array(child1), Genotype.from_array(child2)
