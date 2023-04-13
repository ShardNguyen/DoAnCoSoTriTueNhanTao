import random as rng

# Define the value not present in the input file
mutation_rate = 0.05 # Based on Mr Nguyen Tien Huy lectures on genetic algorithms
population_size = 100 # Population size at the beginning 
num_generations = 3 * population_size# Number of offsprings should be at least 3 times the original population

# Read the input parameters from the Input.txt file

file = open("Input.txt", "r")

max_weight = int(file.readline())
total_class = int(file.readline())
weights = list(map(int, file.readline().strip().split(", ")))
values = list(map(int,file.readline().strip().split(", ")))
classes = list(map(int,file.readline().strip().split(", ")))
class_values = file.read().split("\n")

file.close()


# Define the fitness function
def fitness(chromosome):
    total_value = sum([values[i] for i in range(len(chromosome)) if chromosome[i] == 1])
    total_weight = sum([weights[i] for i in range(len(chromosome)) if chromosome[i] == 1])
    if total_weight > max_weight:
        return 0
    else:
        return total_value

# Define the initialization function
def initialize_population():
    population = []
    for i in range(population_size):
        chromosome = [rng.randint(0, 1) for j in range(len(values))]
        population.append(chromosome)
    return population

# Define the selection function
def select_parents(population):
    fitness_values = [fitness(chromosome) for chromosome in population]
    total_fitness = sum(fitness_values)
    probabilities = [fitness_value / total_fitness for fitness_value in fitness_values]
    parent1_index = rng.choices(range(population_size), weights=probabilities)[0]
    parent2_index = rng.choices(range(population_size), weights=probabilities)[0]
    return population[parent1_index], population[parent2_index]

# Define the crossover function
def crossover(parent1, parent2):
    crossover_point = rng.randint(1, len(values) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Define the mutation function
def mutate(chromosome):
    mutated_chromosome = chromosome[:]
    for i in range(len(chromosome)):
        if rng.random() < mutation_rate:
            mutated_chromosome[i] = 1 - mutated_chromosome[i]
    return mutated_chromosome

# Run the genetic algorithm
population = initialize_population()
for generation in range(num_generations):
    parent1, parent2 = select_parents(population)
    child1, child2 = crossover(parent1, parent2)
    child1 = mutate(child1)
    child2 = mutate(child2)
    population.append(child1)
    population.append(child2)
    population = sorted(population, key=lambda chromosome: -fitness(chromosome))[:population_size]

# Print the best solution
best_solution = max(population, key=fitness)
best_value = fitness(best_solution)

file = open("Output.txt", "w")

""" 
print("Best solution:", best_solution)
print("Best value:", best_value)
"""

file.write(repr(best_value) + "\n")
file.write(repr(best_solution) + "\n")

file.close()