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