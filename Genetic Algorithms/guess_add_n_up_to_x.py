########## guess_add_n_up_to_x.py ##########

'''

- This script adds n numbers up to a target x through a genetic algorithm
- Analysis is provided for a fixed number of generations as well as for running until convergence

'''


#########
# imports
#########

from random import randint, random, uniform, sample, seed
from numpy import cumsum, array
from operator import itemgetter, add
from pandas import DataFrame
from functools import reduce
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


####################
# initial conditions
####################

seed()
n = 10 # number of terms to be added together
x = 7 # target value that sum(n) approaches
min_val = 0 # the minimum value for randint
max_val = 100 # the maximum value for randint
population_size = 100 # number of parents per population
elite_size = 20
mutation_rate = 0.01
generations = 500

#####################################
# define the algorithm implementation
#####################################

def create_parent(n , min_val, max_val):
	parent = [randint(min_val, max_val) for i in range(n)]
	return parent

def create_population(population_size, n ,min_val, max_val):
	population = [create_parent(n ,min_val, max_val) for i in range(population_size)]
	return population

def create_fitness(parent, x):
	sum_parent = cumsum(parent)
	fitness = 1 / (abs(x - sum_parent[-1]))
	return fitness

def rank_population(population):
	fitness_results = {}
	for i in range(len(population)):
		fitness_results[i] = create_fitness(population[i], x)
	return sorted(fitness_results.items(), key = itemgetter(1), reverse = True)

def select_parents(rank, elite_size):
	selection_results = []
	df = DataFrame(array(rank), columns = ['Index', 'Fitness'])
	df['Cum_Sum'] = df.Fitness.cumsum()
	df['Cum_Percent'] = (df.Cum_Sum/df.Fitness.sum())*100
	for i in range(elite_size):
		selection_results.append(rank[i][0])
	for i in range(len(rank) - elite_size):
		pick = 100*random()
		for i in range(len(rank)):
			if pick <= df.iat[i, 3]:
				selection_results.append(rank[i][0])
				break
	return selection_results

def mating_pool(population, selection_results):
	mating_pool = []
	for i in range(len(selection_results)):
		j = selection_results[i]
		mating_pool.append(population[j])
	return mating_pool

def breed_population(mating_pool, elite_size):
	children = []
	length = len(mating_pool) - elite_size
	pool = sample(mating_pool, len(mating_pool))
	for i in range(elite_size):
		children.append(mating_pool[i])
	for i in range(length):
		male = randint(0, length-1)
		female = randint(0, length-1)
		if male != female:
			male = pool[male]
			female = pool[female]
			half = len(male) // 2
			child = male[:half] + female[half:]
			children.append(child)
		else:
			male_ = pool[female]
			female_ = pool[male]
			half = len(male_) // 2
			child = male_[:half] + female_[half:]
			children.append(child)
	return children

def mutate_population(population, mutation_rate):
	mutated_population = []
	for parent in population:
		if random() > mutation_rate:
			mutated_population.append(parent)
		else:
			mutation_position = randint(0, len(parent) - 1)
			parent[mutation_position] = randint(min_val, max_val)
			mutated_population.append(parent)
	return mutated_population

def next_generation(current_generation, elite_size, mutation_rate):
	rank = rank_population(current_generation)
	selection_results = select_parents(rank, elite_size)
	matingpool = mating_pool(current_generation, selection_results)
	children = breed_population(matingpool, elite_size)
	next_generation = mutate_population(children, mutation_rate)
	return next_generation

def genetic_algorithm(population, population_size, elite_size, mutation_rate, generations):
	start_time = datetime.now()
	population = create_population(population_size, n ,min_val, max_val)
	print('Running with a fixed amount of generations...'); print('\n'); print('Initial Guess:', population[0]); print('sum(guess) - target =', (x - reduce(add, population[0], 0))); print('\n')
	for i in range(generations):
		population = next_generation(population, elite_size, mutation_rate)
	print('Final Guess:', population[0]); print('sum(guess) - target =', (x - reduce(add, population[0], 0))); print('\n'); print('Elapsed Time:', datetime.now() - start_time)
	print('\n')
	population = create_population(population_size, n ,min_val, max_val)
	generations = 1
	print('Running until convergence...'); print('\n'); print('Initial Guess:', population[0]); print('sum(guess) - target =', (x - reduce(add, population[0], 0))); print('\n')
	while (x - reduce(add, population[0], 0)) != 0:
		population = next_generation(population, elite_size, mutation_rate)
		generations += 1
	print('Final Guess (in ' + str(generations) + ' generations) :', population[0]); print('sum(guess) - target =', (x - reduce(add, population[0], 0))); print('\n'); print('Elapsed Time:', datetime.now() - start_time)


##################################################
# solve and visualize the algorithm implementation
##################################################

population = create_population(population_size, n ,min_val, max_val)
GA = genetic_algorithm(population = population, population_size = population_size, elite_size = elite_size, mutation_rate = mutation_rate, generations = generations)