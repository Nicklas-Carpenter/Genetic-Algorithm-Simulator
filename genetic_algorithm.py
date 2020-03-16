import math
import csv
import random
import configparser
import argparse
import probability

from Bitstring import Bitstring

# TODO: Consider Selection
#   - Proportional to fitness
#   - Proportional to average fitness
#   - Proportional to rank (fitness = max - rank)

# TODO: Consider step fitness function with cutoff
# Step-function cut-off

FIELD_NAMES = ["generation", "max", "average", "min", "best"]

population = []

def gene_comparative_fitness_func(genes):
    '''Function used to measure the fitness of a new generation'''

    fitness = 0;

    for i in range(len(genes)):
        if genes[i] == 1:
            fitness += 1

    if PROBABALISTIC_FITNESS_FUNCTION:
        noise = -1
        while noise > 1 or noise < 0:
            noise = NOISE()
        return fitness * noise

    return fitness

def generate_initial_population():
    '''Establishes the initialize bitstring population by generation of random
    bitstrings'''

    for i in range(POPULATION_SIZE):
        population.append(Bitstring(BITSTRING_SIZE, FITNESS_FUNCTION))

def repopulate():
    '''Function used to generate a new generation'''

    for i in range(math.ceil(POPULATION_SIZE * REPOPULATION_RATIO)):
        if CROSSOVER:
            population[POPULATION_SIZE - i - 1] = Bitstring.crossover(
                population[random.randint(
                    0, 
                    POPULATION_SIZE * REPOPULATION_RATIO
                )],
                population[random.randint(
                    0, 
                    POPULATION_SIZE * REPOPULATION_RATIO
                )],
            )
        if MUTATE:
            population[POPULATION_SIZE - i - 1].mutate()

def fitness_comparator(phenotype):
    return MAX_FITNESS - phenotype.get_current_fitness()

def get_average_fiteness():
    '''Finds the average fitness of the population'''

    cumulative_fitness = 0

    for i in range(POPULATION_SIZE):
        cumulative_fitness += population[i].get_current_fitness()
    
    return math.floor(cumulative_fitness / POPULATION_SIZE)

def make_generation_summary(writer, generation):
    '''Generate an statistics summary for the current bitstream generation'''
    
    # TODO: Format for PEP8
    writer.writerow({
                        "generation": generation,
                        "max": population[0].get_current_fitness(),
                        "average": get_average_fiteness(),
                        "min": population[POPULATION_SIZE - 1].get_current_fitness(),
                        "best": population[0].get_bitstring()
    })


##### Main #####

### Initialize configurations ###
parser = argparse.ArgumentParser()
parser.add_argument("config_file")

args = parser.parse_args()

with open(args.config_file, mode='r', newline = '') as config_file :
    config = configparser.ConfigParser()
    config.read_file(config_file)

    ## Initialize parameters
    MAX_GENERATIONS = config.getint("PARAMETERS", "MAX_GENERATIONS")
    BITSTRING_SIZE = config.getint("PARAMETERS", "BITSTRING_SIZE")
    REPOPULATION_RATIO = config.getfloat("PARAMETERS", "REPOPULATION_RATIO")
    OUTPUT_FILE = config.get("PARAMETERS", "OUTPUT_FILE")
    SEED = int(config.get("PARAMETERS", "SEED"), base = 16)
    POPULATION_SIZE = config.getint("PARAMETERS", "POPULATION_SIZE")

    ## Set up fitness function ##
    PROBABALISTIC_FITNESS_FUNCTION = config.getboolean(
        "OPTIONS",
        "PROBABALISTIC_FITNESS_FUNCTION"
    )

    fitness_function = config.get("PARAMETERS", "FITNESS_FUNCTION")
    if fitness_function == "GENE_COMPARATIVE":
        FITNESS_FUNCTION = gene_comparative_fitness_func
        MAX_FITNESS = BITSTRING_SIZE
    elif fitness_function == "GRADE_SQUARED":
        MAX_FITNESS = 1.0
    else:
        exit() # TODO: Throw an error

    CROSSOVER = config.getboolean("OPTIONS", "CROSSOVER")
    MUTATE = config.getboolean("OPTIONS", "MUTATE")
    # TODO: Incorporate average fitness functionality
    USE_AVERAGE_FITNESS = config.getboolean("OPTIONS", "USE_AVERAGE_FITNESS")

    ## Configure possibility of random elements in fitness ##
    if config.getboolean("OPTIONS", "PROBABALISTIC_FITNESS_FUNCTION"):
        distribution = config.get("PARAMETERS", "PROBABILITY_DISTRIBUTION")
        if distribution == "UNIFORM":
            a = config.getfloat("UNIFORM", "A")
            b = config.getfloat("UNIFORM", "B")
            NOISE = probability.create_uniform_generator(a, b)
        elif distribution == "NORMAL":
            lam = config.getfloat("EXPONENTIAL", "LAMBDA")
            NOISE = probability.create_exponential_generator(lam)
        elif distribution == "EXPONENTIAL":
            mu = config.getfloat("GAUSS", "MU")
            sigma = config.getfloat("GAUSS", "SIGMA")
            NOISE = probability.create_gauss_generator(mu, sigma)
        else:
            exit() # TODO: Throw an error

    ## Determine repopulation method ##
    # TODO: Implement microbial genetic algorithm
    repopulation_method = config.read("PARAMETERS", "REPOPULATION_METHOD")
    if repopulation_method == "DEFAULT":
        pass
    elif repopulation_method == "MICROBIAL":
        pass
    else:
        pass

    config_file.close()

### Genetic Algorithm ### 
random.seed(SEED)
generation = 0

generate_initial_population()

with open(OUTPUT_FILE, mode='w', newline = '') as summary_file:
    writer = csv.DictWriter(summary_file, fieldnames=FIELD_NAMES)
    writer.writeheader()

    while (generation < MAX_GENERATIONS) \
           and (population[0].get_current_fitness() < MAX_FITNESS):
        repopulate();
        population = sorted(population, key=fitness_comparator)
        make_generation_summary(writer, generation)
        generation += 1
    summary_file.close()