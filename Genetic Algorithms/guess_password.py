########## guess_password.py ##########

'''

- This script guesses a secret password through a genetic algorithm (not conventional - no breeding of a population from a mating pool)
- The algorithm creates a parent, mutates it by randomly swapping characters in the parent, and the child becomes the parent
- Fitness is defined as how many chars in the parents match the position of chars in the target
- If fitness(child) > fitness(parent), child = parent

'''

#########
# imports
#########

from random import sample, seed, randrange, choice
from datetime import datetime

####################
# initial conditions
####################

gene_set = " 1234567890acedefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.?_-" # gene set to use for building guesses
target = "Password123!" # target password
max_fitness = len(target)
start_time = datetime.now() # determine the current time
seed() # initialize the pseudorandom number generator in python to the current time

#####################################
# define the algorithm implementation
#####################################

def create_parent():
	''' generate a random string from the gene_set '''
	parent = ''.join([choice(gene_set) for _ in range(len(target))]) # a random string of characters from the gene_set of len(target)
	return parent

def get_fitness(parent):
	''' fitness = total number of letters in the guess that match the letter in the same position as the password '''
	fitness =  sum(1 for expected, actual in zip(target, parent) if expected == actual) # starting at zero, increment the fitness by 1 if the indexed char in guess == indexed char in target
	return fitness

def mutate(parent):
	''' mutate the parent - the child is the mutation of the parent '''
	i = randrange(0, len(parent)) # create a random number from 0 to len(parent)
	child_genes = list(parent) # convert parent to a list, called child_genes
	new_gene, alternate = sample(gene_set, 2) # newGene and alternate are random chars from the gene_set
	child_genes[i] = alternate if new_gene == child_genes[i] else new_gene # randomly indexed char in child_genes becomes new_gene unless if that indexed char is already the new_gene, it becomes alternate
	child = ''.join(child_genes)
	return child # returns the string of chars that has been mutated to include the new_gene

#######################################################
# implement the genetic algorithm and visualize results
#######################################################

parent = create_parent() # create random string of chars from gene_set of len(target) [initial guess]
guesses = 1 # number of guesses that have taken place (= 1 because the only guess so far has been the initial guess)
fitness = get_fitness(parent) # obtain the fitness score of the initial guess of random chars
print('Running Genetic Algoithm:', '\n')
print("{}\t{}\t{}\t{}\t{}".format('Parent: ' + parent, '|', 'Fitness: ' + str(fitness), '|', 'Elapsed Time: ' + str((datetime.now() - start_time))))
while fitness < max_fitness:
	child = mutate(parent)
	child_fitness = get_fitness(child) 
	if fitness >= child_fitness:
		guesses += 1 # a guess has taken place, incremement guesses
		continue
	else:
		guesses += 1 # a guess has taken place, incremement guesses
		parent = child
		fitness = child_fitness
		print("{}\t{}\t{}\t{}\t{}".format('Parent: ' + parent, '|', 'Fitness: ' + str(fitness), '|', 'Elapsed Time: ' + str((datetime.now() - start_time))))
print('\n')
print("{}\t{}\t{}".format('Number of Guesses: ' + str(guesses), '|', 'Total Elapsed Time: ' + str((datetime.now() - start_time))))
print('\n')



