import os
import time
import psutil

from BranchAndBound import BranchAndBoundKnapsack
from LocalBeamSearch import localBeamKnapsack
from BruteForce import bruteForceKnapsack
from Genetic import GeneticKnapsack


# READ DATA FROM FILES
def loadInputFile(input_file: str) -> list[float, int, list[float], list[int], list[int]]:
    with open(input_file, 'r') as fin:
        W = float(fin.readline().strip())
        m = int(fin.readline().strip())
        w = list(map(float, fin.readline().strip().split(', ')))
        v = list(map(int, fin.readline().strip().split(', ')))
        c = list(map(int, fin.readline().strip().split(', ')))
    if(len(v) != len(c) or len(v) != len(w)):
        print("invalid input")
    return W, m, w, v, c

# READING AND WRITING DATA

print("1. Brute force")
print("2. Branch and bound")
print("3. Local beam search")
print("4. Genetic algorithm")

choice = int(input("Alogrithm: "))
KnapsackSolution = bruteForceKnapsack
if choice == 1:
    KnapsackSolution = bruteForceKnapsack
elif choice == 2:
    KnapsackSolution = BranchAndBoundKnapsack
elif choice == 3:
    KnapsackSolution = localBeamKnapsack
elif choice == 4:
    KnapsackSolution = GeneticKnapsack
print("")
temp = input("Please input the list of sequence number of the test case: ")
listNumber = temp.split()

while listNumber:
    x = int(listNumber.pop(0))
    in_path = 'INPUT/INPUT_' + str(x) + '.txt'

    # Reading data from files
    if os.path.isfile(in_path): # Check if input file does exist
        W, m, w, v, c = loadInputFile(in_path)


        process = psutil.Process()

        # Solving Knapsack problem
        start = time.time()
        max_value, bestSol = KnapsackSolution(W, w, v, c, m)
        end = time.time()
        print("----------------------")
        print(in_path)
        print("Runnning time: ", (end - start) * 10**3, " ms")
        process = psutil.Process()
        print("Memory usage: ", process.memory_info().rss, " Byte")
        # Output the best profit
        if(max_value == -1):
            print("\nCannot find the solution")
            out_path =  'OUTPUT/' + 'OUTPUT_' + str(x) +  '.txt'
            with open(out_path, 'w') as fout:
                fout.write("No solution found")
            
        else:
            print("\nFinal profit: ", max_value)
            # Writing data to files
            out_path =  'OUTPUT/' + 'OUTPUT_' + str(x) +  '.txt'
            with open(out_path, 'w') as fout:
                fout.write(str(max_value) + '\n')
                fout.write(', '.join(str(i) for i in bestSol))
            print("Successfully write data to output file!")
        print("----------------------")
    # Input file doesn't exist (User enters a)
    else: 
        print("Error! Input file does not exist.\n")
        continue