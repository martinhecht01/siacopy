import json
import os
from Config import Config
from cli import get_population
from cli import get_genotypes
from cli import execute_crossover
from cli import execute_mutation
from cli import execute_selection
from cli import execute_replacement
from cli import cutoff
from pandas import DataFrame
from src.classes.characters.CharacterABC import CharacterABC
from src.utils.ConfigUtils import ConfigUtils

CONFIG_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, "config.json")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
    characters = config["benchmarks"]["best_mutation"]["characters"]
    mutation_methods = config["benchmarks"]["best_mutation"]["mutations"]
    iterations = config["benchmarks"]["best_mutation"]["iterations"]

config = Config(CONFIG_PATH)


def best_mutation_df():
    rows = []

    for character in characters:
        for iteration in range(1, iterations + 1):
            for mutation in mutation_methods:
                
                generation = get_population(config.genotypes, ConfigUtils.CHARACTERS[character])
                generation_count = 0
                oldPopulations = []

                while cutoff(generation, oldPopulations, config.cutoff_parameter, generation_count, config.cutoff) is False:
                    selection = execute_selection(generation, config.individuals, config.first_selection,
                                                  config.second_selection, config.a_value)
                    selection_genotypes = get_genotypes(selection)
                    crossover_genotypes = execute_crossover(selection_genotypes, config.crossover)
                    mutated_genotypes = execute_mutation(crossover_genotypes, ConfigUtils.MUTATION[mutation],
                                                         config.mutation_probability)
                    children = get_population(mutated_genotypes, ConfigUtils.CHARACTERS[character])
                    generation = execute_replacement(generation, children, config.replacement_type,
                                                     config.replacement_first_selection,
                                                     config.replacement_second_selection, config.b_value)
                    generation_count += 1
                    oldPopulations.append(generation)

                best: CharacterABC = max(generation)
                rows.append({"iteration": iteration, "character": character, "method": mutation,
                             "fitness": best.fitness(), "generation": generation_count})

    return DataFrame(rows)
