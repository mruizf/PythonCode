'''
Created on 23/07/2016

@author: M R
'''
#Differential evolution
#Individual representation
#
#
import numpy as np
import random


class Population(object):
    def __init__(self,size_population,size_individual,min_values,max_values,aptitudMethod):

        len_max =len(max_values)
        len_min =len(min_values)

        if len_max != len_min or len_max <= 0 :
            print("Error of conditions")

        #This for Python 3 compatibility        
        self.limits = list(zip(min_values,max_values))

        value = lambda pair_min_max:  pair_min_max[0] + random.random()* (pair_min_max[1]-pair_min_max[0])

        row_init = lambda x: [value(i) for i in self.limits]
                     
        array_list = [row_init(i) for i in range(size_population)]

        #First population        
        self.population = np.array(array_list)

        self.aptitud = aptitudMethod

        self.aptitudes = [aptitudMethod(individual) for individual in self.population]        
        
        
class Evolutive:
        
    def __init__(self, num_iterationes,population, prob_mutation, F ):
        
        self.num_iterationes = num_iterationes
        self.population = population
        self.prob_mutation = prob_mutation 
        self.F = F
    
    def iteration(self):
        
        indexes = list(range(0,len(self.population.population)))
        
        size_individual = len(self.population.population[0])
        
        for index,individual in enumerate(self.population.population):
            
            #Take the 3 random elements, for recombination, diffents each other and the individual selected
            indexes.remove(index)
            
            indexes_mutation = random.sample(indexes, 3)
                        
            a = self.population.population[indexes_mutation[0]]
            b = self.population.population[indexes_mutation[1]]
            c = self.population.population[indexes_mutation[2]]
            
            R = random.randint(0,size_individual-1)
            y = np.array(individual)
            for i in range(size_individual):
                if random.random() < self.prob_mutation or i == R:
                    y[i] =a[i]+self.F*(b[i]-c[i])
            
            if self.population.aptitud(y) < self.population.aptitud(individual):
                self.population.population[index] = y
                self.population.aptitudes[index] = self.population.aptitud(y)
                
            indexes.insert(index, index)
            
    def main(self):
        
        y0 = min(self.population.aptitudes)
        print("Iteration ",0,":",y0)
        counter = 0
        
        while True:
            self.iteration()
            y1 = min(self.population.aptitudes)
            ind = self.population.aptitudes.index(y1)
            
            #if (abs(y1-y0) < 0.00001 or counter>= self.num_iterationes):
            if (counter>= self.num_iterationes):
                break;
            y0 = y1
            counter += 1 
            print("Iteration ",counter,":",self.population.population[ind]," ",y0)
        return min(self.population.aptitudes)
                    
def Rosenbrock(x): 
    return (1-x[0])**2 + 100*(x[1]-x[0]**2)**2


if __name__ == '__main__':
    
    #def __init__(self,size_population,size_individual,min_values,max_values):    
    poblation = Population(10,2,[-1,-1],[1,2],Rosenbrock)

    #def __init__(self, num_iterationes,population, prob_mutation, F ):
    evolutive = Evolutive(1000, poblation, 0.5, 0.5)

    print("Resultado: ",evolutive.main())