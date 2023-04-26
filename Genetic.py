import random as rng

# Define the value not present in the input file

# Read the input parameters from the Input.txt file

# file = open("INPUT_1.txt", "r")

# max_weight = int(file.readline())
# total_class = int(file.readline())
# weights = list(map(int, file.readline().strip().split(", ")))
# values = list(map(int,file.readline().strip().split(", ")))
# classes = list(map(int,file.readline().strip().split(", ")))
# class_values = file.read().split("\n")

# file.close()



# Define the fitness function
def fitness(chromosome, values, weights, classes, max_weight, num_of_class):
    total_fitness = 0
    total_weight = 0
    available_class = 0
    big_num = 0 # For fitness calculation
    
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_fitness += values[i]
            total_weight += weights[i]
            available_class |= 1 <<(classes[i] - 1) # Shift bit
        big_num += values[i]
    if total_weight <= max_weight:
        total_fitness += 2 * big_num 
    if available_class == (2**num_of_class - 1): # 111 = 7
        total_fitness += big_num
    #if total_weight > max_weight: Because we already have the big_num value so return is not needed
        #return 0  # penalize solutions that exceed the maximum weight limit
    return total_fitness

def checkSatifyConstraint(chromosome, values, weights, classes, max_weight, num_of_class):
    total_value = 0
    total_weight = 0
    available_class = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += values[i]
            total_weight += weights[i]
            available_class |= 1 <<(classes[i] - 1) # Shift bit
    if total_weight > max_weight: #exceed weight
        return -1
    if available_class != (2**num_of_class - 1): #there is at least one class not have items
        return -1
    return total_value
# Define the initialization function

""" def initialize_population():
    population = []
    for _ in range(population_size):
        chromosome = [rng.randint(0, 1) for _ in range(len(values))]
        population.append(chromosome)
    return population """


def initialize_population(population_size, values, weights, max_weight):
    population = []
    population.append([0] * len(values)) # set bang 0 het de gioi han
    for _ in range(population_size - 1):
        chromosome  = []
        totalWeight = 0
        for j in range(len(values)):
            if(totalWeight < max_weight):
                randNum = rng.choices([0, 1], weights=[5, 5], k = 1)[0]
            else:
                randNum = rng.choices([0, 1], weights=[8, 2], k = 1)[0]
            chromosome.append(randNum)
            if(randNum == 1):
                totalWeight += weights[j]
        population.append(chromosome)
    return population

# Replace the old selection algo with tournament selection
# Define the selection function
def tournament_selection(population, values, weights, classes, max_weight, num_of_class):
    k = 5 
    selected = []
    for i in range(len(population)):
        contestants = rng.sample(population, k)
        winner = max(contestants, key=lambda x: fitness(x, values, weights, classes, max_weight, num_of_class))
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
def elitist_replacement(population, offspring_population, population_size, values, weights, classes, max_weight, num_of_class):
    all_population = population + offspring_population
    sorted_population = sorted(all_population, key=lambda x: fitness(x, values, weights, classes, max_weight, num_of_class), reverse=True)
    return sorted_population[:population_size]



def GeneticKnapsack(max_weight, weights, values, classes, m):
    #population_size MUST be EVEN
    population_size = 100 # Population size at the beginning 
    num_generations = 3 * population_size# Number of offsprings should be at least 3 times the original population
    mutation_rate = 0.05 # Based on Mr Nguyen Tien Huy lectures on genetic algorithms
    
    # Initialize the population
    population = initialize_population(population_size, values, weights, max_weight)

    # Evolution loop
    for i in range(num_generations):
        # Selection
        parents = tournament_selection(population, values, weights, classes, max_weight, m)

        # Crossover
        offspring_population = []   
        for j in range(0, population_size, 2):
            offspring1, offspring2 = binary_crossover(parents[j], parents[j+1])
            offspring_population.append(offspring1)
            offspring_population.append(offspring2)

        # Mutation
        for j in range(len(offspring_population)):
            offspring_population[j] = binary_mutation(offspring_population[j], mutation_rate)


        # #Evaluate fitness
        # for j in range(len(offspring_population)):
        #     fitnessList.append(fitness(offspring_population[j])

        # Replacement
        population = elitist_replacement(population, offspring_population, population_size, values, weights, classes, max_weight, m)

    # Print the best solution found
    best_solution = population[0]

    totalVal = checkSatifyConstraint(best_solution, values, weights, classes, max_weight, m)
    if(totalVal == -1): #the solution commit the rule
        return -1, []
    return totalVal, best_solution
