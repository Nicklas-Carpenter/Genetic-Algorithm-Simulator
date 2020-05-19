# genetic_algorithm.py - Runs a user-modifiable genetic algorithm on bitstrings
# Copyright (C) 2020  Nicklas Carpenter

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math
import csv
import configparser
import argparse
import probability
import numpy as np

from Bitstring import Bitstring
from random import random, randint, seed
from multiprocessing import Process
from multiprocessing.sharedctypes import Array
from multiprocessing.managers import SharedMemoryManager

# TODO Consider Selection
#   - Proportional to fitness
#   - Proportional to average fitness
#   - Proportional to rank (fitness = max - rank)

# TODO Consider step fitness function with cutoff
# Step-function cut-off

# TODO Store fitness ina seperate array

FIELD_NAMES = ["generation", "max", "average", "min", "best"]

N = 1000

TARGET_W = np.pi
TARGET = []
SINUSOIDS = []

BITSTRING = []

def fitness_func(index, genes, fitness, sinusoids, target):
    '''Function used to measure the fitness of a new generation'''
    
    error = 1.0

    x = np.zeros(N)

    for i, gene in enumerate(genes):
        x += gene * sinusoids[i]
    
    for i in range(N):
        expected = target[i]

        actual = x[i]
        error += np.fabs(expected - actual)

    fitness[index] = 1.0 / error


def calculate_fitness():
    processes = []
    fitnesses = Array("f", POPULATION_SIZE)

    for index, individual in enumerate(BITSTRING):
        process = Process(
            target = fitness_func, 
            args = (
                index, individual.get_bitstring(), 
                fitnesses,
                SINUSOIDS,
                TARGET
            ) 
        )

        process.start()
        processes.append(process)

    for index, individual in enumerate(BITSTRING):
        processes[index].join()
        individual.fitness = fitnesses[index]



# Bitstring size + 1 since we are ignoring w = w_target
def generate_sinusoids():
    smm = SharedMemoryManager()
    smm.start()

    W = []
    increment = 1.5 / (BITSTRING_SIZE + 1) 

    t = np.linspace(0, (4 * np.pi) / TARGET_W, N)

    for i in range(BITSTRING_SIZE + 1):
        if (0.5 + i * increment) == 1:
            continue

        w = TARGET_W / (0.5 + i * increment)
        W.append(w)
        SINUSOIDS.append(0.25 * np.cos(w * t))
    
    TARGET = np.cos(TARGET_W * t)


    w_list = ""
    freqs = open("frequencies.ini", "w")
    for i in range(BITSTRING_SIZE):
        w_list += str(W[i]) + ","

    w_list = w_list[0: len(w_list) - 2]

    records = {
        "DEFAULT": {
            "frequencies": str(w_list),
            "target": TARGET_W
        }
    }

    record = configparser.ConfigParser()
    record.read_dict(records)
    record.write(freqs)

    freqs.close()


def generate_initial_population():
    '''Establishes the initialize bitstring population by generation of random
    bitstrings'''

    for i in range(POPULATION_SIZE):
        BITSTRING.append(Bitstring(BITSTRING_SIZE))

def repopulate():
    '''Function used to generate a new generation'''

    elite_end = math.ceil(POPULATION_SIZE * REPOPULATION_RATIO) - 1

    for i in range(elite_end + 1, len(BITSTRING)):
        if CROSSOVER:
            BITSTRING[i] = Bitstring.crossover(
                BITSTRING[randint(0, elite_end)],
                BITSTRING[randint(0, elite_end)]
            )
            
        if MUTATE:
            BITSTRING[i].mutate()

def fitness_comparator(phenotype):
    return phenotype.fitness


def get_average_fiteness():
    '''Finds the average fitness of the population'''

    cumulative_fitness = 0

    for i in range(POPULATION_SIZE):
        cumulative_fitness += BITSTRING[i].fitness
    
    return cumulative_fitness / POPULATION_SIZE

def make_generation_summary(writer, generation):
    '''Generate an statistics summary for the current bitstream generation'''
    
    # TODO Format for PEP8
    writer.writerow({
        "generation": generation,
        "max": BITSTRING[0].fitness,
        "average": get_average_fiteness(),
        "min": BITSTRING[POPULATION_SIZE - 1].fitness,
        "best": BITSTRING[0].get_bitstring()
    })


##### Main #####

### Initialize configurations ###
parser = argparse.ArgumentParser()
parser.add_argument("config_file")

args = parser.parse_args()

config_file = open(args.config_file, mode='r', newline = '')
config = configparser.ConfigParser()
config.read_file(config_file)

## Initialize parameters
MAX_GENERATIONS = config.getint("PARAMETERS", "MAX_GENERATIONS")
BITSTRING_SIZE = config.getint("PARAMETERS", "BITSTRING_SIZE")
REPOPULATION_RATIO = config.getfloat("PARAMETERS", "REPOPULATION_RATIO")
OUTPUT_FILE = config.get("PARAMETERS", "OUTPUT_FILE") + ".csv"
SEED = int(config.get("PARAMETERS", "SEED"), base = 16)
POPULATION_SIZE = config.getint("PARAMETERS", "POPULATION_SIZE")

## Set up fitness function ##
PROBABALISTIC_FITNESS_FUNCTION = config.getboolean(
    "OPTIONS",
    "PROBABALISTIC_FITNESS_FUNCTION"
)

CROSSOVER = config.getboolean("OPTIONS", "CROSSOVER")
MUTATE = config.getboolean("OPTIONS", "MUTATE")

## Determine repopulation method ##
# TODO Implement microbial genetic algorithm
repopulation_method = config.read("PARAMETERS", "REPOPULATION_METHOD")
if repopulation_method == "DEFAULT":
    pass
elif repopulation_method == "MICROBIAL":
    pass
else:
    pass

config_file.close()

### Genetic Algorithm ### 
seed(SEED)
generation = 0

generate_sinusoids()
generate_initial_population()

summary_file = open(OUTPUT_FILE, mode = "w", newline = "")
writer = csv.DictWriter(summary_file, fieldnames = FIELD_NAMES)
writer.writeheader()

while (generation < MAX_GENERATIONS):
    print("Generation {0}".format(generation))
    calculate_fitness()
    make_generation_summary(writer, generation)
    BITSTRING.sort(key = fitness_comparator, reverse = True)
    generation += 1
    repopulate()
    
summary_file.close()

