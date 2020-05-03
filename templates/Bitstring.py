# Bitstring.py - A string of bits that the genetic algorithm optimizes
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

import random

class Bitstring:
    '''A bitstring class used to test genetic algorithm variations'''

    @classmethod
    def crossover(cls, a, b):
        '''Generate a child bitstrin from sexual reproduction'''

        genes = []
        donor = a

        for i in range(a.__bitstring_size):
            genes.append(donor.get_bitstring()[i])
            if random.randint(1, 5) == 5:
                if donor == a:
                    donor = b
                else: 
                    donor = a 
    
        return cls(a.__bitstring_size, a.__fitness_func, dna = genes)

    def __init__(self, bitstring_size, fitness_func, dna=False):
        self.__bitstring = []
        self.__fitness_scores = []
        self.__current_fitness = 0
        self.__age = 0
        self.__bitstring_size = bitstring_size
        self.__fitness_func = fitness_func

        if dna:
            self.__set_bitstring(dna)
        else:
            self.__generate_bitstring()
        
        self.__calculate_fitness()

    def __generate_bitstring(self):
        for i in range(self.__bitstring_size):
            self.__bitstring.append(random.randint(0, 1))
    
    def __calculate_fitness(self):
        self.__current_fitness = self.__fitness_func(self.__bitstring)
        self.__fitness_scores.append(self.__current_fitness)
        self.__age += 1

    def mutate(self):
        '''Modify genes through random mutation'''
        for i in range(self.__bitstring_size):
            if random.randint(0, 100) == 100:
                self.__bitstring[i] = abs(self.__bitstring[i] - 1)
        
        self.__calculate_fitness()
                

    def __set_bitstring(self, bitstring):
        self.__bitstring = bitstring
        
    def get_current_fitness(self):
        return self.__current_fitness

    def get_average_fitness(self):
        return self.__average_fitness
    
    def get_bitstring(self):
        return self.__bitstring