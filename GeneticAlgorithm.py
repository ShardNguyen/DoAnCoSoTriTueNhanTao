import random as rng

# Define the value not present in the input file
# Dieu chinh pop dua vao 
mutation_rate = 0.05 # Based on Mr Nguyen Tien Huy lectures on genetic algorithms
population_size = 100 # Population size at the beginning 
num_generations = 20 * population_size# Number of offsprings should be at least 3 times the original population
# Read the input parameters from the Input.txt file

file = open("INPUT_1.txt", "r")

max_weight = int(file.readline())
total_class = int(file.readline())
weights = list(map(int, file.readline().strip().split(", ")))
values = list(map(int,file.readline().strip().split(", ")))
classes = list(map(int,file.readline().strip().split(", ")))
class_values = file.read().split("\n")

file.close()

big_num = sum([values[i] for i in range(len(values))]) # For fitness calculation

# Define the fitness function
def fitness(chromosome):
    total_fitness = 0
    total_weight = 0
    availibe_class = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_fitness += values[i]
            total_weight += weights[i]
            availibe_class |= 1 <<(classes[i] - 1) # Shift bit
    if total_weight <= max_weight:
        total_fitness += 2 * big_num 
    if availibe_class == (2**total_class - 1): # 111 = 7
        total_fitness += big_num
    #if total_weight > max_weight: Because we already have the big_num value so return is not needed
        #return 0  # penalize solutions that exceed the maximum weight limit
    return total_fitness

def cal_value(chromosome):
    total_value = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += values[i]
    return total_value

# Define the initialization function

""" def initialize_population():
    population = []
    for _ in range(population_size):
        chromosome = [rng.randint(0, 1) for _ in range(len(values))]
        population.append(chromosome)
    return population """

#by MQ with love 
def initialize_population(): # Init gioi han so vat trong list, do test case thuong chi can 1 toi 3 vat la du weight
    population = []
    population.append([0] * len(values)) # set bang 0 het de gioi han
    for _ in range(population_size - 1):
        chromosome  = []
        totalWeight = 0
        for j in range(len(values)):
            randNum = rng.choices([0, 1], weights=[totalWeight, max_weight], k = 1)[0]
            chromosome.append(randNum)
            if(randNum == 1):
                totalWeight += weights[j]
        population.append(chromosome)
    return population

# Replace the old selection algo with tournament selection
# Define the selection function
def tournament_selection(population, k=5):
    selected = []
    for i in range(len(population)):
        contestants = rng.sample(population, k)
        winner = max(contestants, key=lambda x: fitness(x))
        selected.append(winner)
    return selected

# Define the crossover function
def binary_crossover(parent1, parent2):
    crossover_point = rng.randint(0, len(parent1) - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

# Define the mutation function
def binary_mutation(chromosome, rate):
    for i in range(len(chromosome)):
        if rng.random() < rate:
            chromosome[i] = 1 - chromosome[i]  # flip bit
    return chromosome

# Define the elitist replacement function
def elitist_replacement(population, offspring_population):
    all_population = population + offspring_population
    sorted_population = sorted(all_population, key=lambda x: fitness(x), reverse=True)
    return sorted_population[:population_size]

# Initialize the population
population = initialize_population()

# Evolution loop
for i in range(num_generations):
    # Selection
    parents = tournament_selection(population)

    # Crossover
    offspring_population = []
    for j in range(0, population_size, 2):
        offspring1, offspring2 = binary_crossover(parents[j], parents[j+1])
        offspring_population.append(offspring1)
        offspring_population.append(offspring2)

    # Mutation
    for j in range(len(offspring_population)):
        offspring_population[j] = binary_mutation(offspring_population[j], mutation_rate)

    # Evaluate fitness
    for j in range(len(offspring_population)):
        fitness(offspring_population[j])

    # Replacement
    population = elitist_replacement(population, offspring_population)

# Print the best solution found
best_solution = max(population, key=lambda x: fitness(x))
print(f"Best solution: {best_solution}")
print(f"Best value: {cal_value(best_solution)}")