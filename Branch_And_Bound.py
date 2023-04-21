from collections import deque
from typing import List, Tuple
import os

def loadInputFile(input_file: str) -> Tuple[int, int, List[float], List[int], List[int]]:
    with open(input_file, 'r') as fin:
        W = float(fin.readline().strip())
        m = int(fin.readline().strip())
        w = list(map(float, fin.readline().strip().split(', ')))
        v = list(map(int, fin.readline().strip().split(', ')))
        c = list(map(int, fin.readline().strip().split(', '))) 
        """W = float(fin.readline())
        m = int(fin.readline())
        w = list(map(float, fin.readline().split(', ')))
        v = list(map(int, fin.readline().split(', ')))
        c = list(map(int, fin.readline().split(', ')))"""
    return W, m, w, v, c

class Item:
    def __init__(self, weight: int, value: int, class_label: int, first_index: int):
        self.weight = weight
        self.value = value
        self.ratio = value / weight
        self.class_label = class_label
        self.first_index = first_index

class KnapsackNode:
    def __init__(self, weight: int, profit: int, level: int, bound: int, class_select: int, choose: str):
        self.weight = weight
        self.profit = profit
        self.level = level
        self.bound = bound
        self.class_select = class_select
        self.choose = choose

def getBound(Node, n, W, Item_list, m):
    if Node.weight >= W:
        return 0
    
    check_class = Node.class_select
    # present_level = Node.level
    next_level = Node.level + 1
    while (next_level < n):
        check_class |= (1 << (Item_list[next_level].class_label - 1))
        next_level += 1
    
    if (2**m - 1 != check_class):
        return 0

    profit_bound = Node.profit

    j = Node.level + 1 # Check all the nodes in the future
    totalWeight = Node.weight

    while ((j < n) and (totalWeight + Item_list[j].weight <= W)):
        totalWeight += Item_list[j].weight
        profit_bound += Item_list[j].value
        j += 1
    
    if j < n:
        profit_bound += (W - totalWeight) * Item_list[j].value / Item_list[j].weight

    #check class

    return profit_bound

def Knapsack(W, weights, values, class_label, num_of_class):
    
    Item_list = []

    for index, value in enumerate(values):
        Item_list.append(Item(weights[index], values[index], class_label[index], index))

    Item_list.sort(key = lambda x:x.ratio, reverse=True)

    stack = [KnapsackNode(0, 0, -1, -1, 0, '')]
    n = len(values)
    maxProfit = 0
    best_string = ''
    while stack:
        u = stack.pop()
        
        if u.level == n-1:
            continue

        nextLevel = u.level + 1
        
        withoutItem = KnapsackNode(u.weight, u.profit, nextLevel, 0, u.class_select, '')
        withoutItem.bound = getBound(withoutItem, n, W, Item_list, num_of_class)
        withoutItem.choose = u.choose + '0'
        
        if withoutItem.bound > maxProfit:
            stack.append(withoutItem)
        # parent_classSelect = u.class_select
        # child_classSelect = parent_classSelect | (1 << (Item_list[nextLevel].class_label - 1))
        withItem = KnapsackNode(u.weight + Item_list[nextLevel].weight, u.profit + Item_list[nextLevel].value, nextLevel, 0, u.class_select | (1 << (Item_list[nextLevel].class_label - 1)), '')
        withItem.bound = getBound(withItem, n, W, Item_list, m)
        withItem.choose = u.choose + '1'

        if (withItem.weight <= W and withItem.profit > maxProfit and (2**num_of_class - 1 == withItem.class_select)):
            maxProfit = withItem.profit
            best_string = withItem.choose

        if withItem.bound > maxProfit:
            """if (withItem.weight <= W and withItem.profit > maxProfit and (2**m - 1 == withItem.class_select)):
                maxProfit = withItem.profit
                best_string = withItem.choose"""
            stack.append(withItem)
        
    temp = []
    for i in range(0, n):
        temp.append(0)

    # 0 1 1 : best string
    # 1 0 1 : temp

    for i in range(0, len(best_string)):
        if best_string[i] == '1':
            temp[Item_list[i].first_index] = 1
        
    return maxProfit, temp

# MENU
x = -10

while x != 0:
    temp = input("Please input the sequence number of the test case: ")

    # Incorrect input type (string, empty input, negative number, etc...)
    if temp.isnumeric() == False:
        print("Wrong input type! The input must be a positive number\n")
        continue
    
    x = int(temp)

    """ Stop the program if the user enters 0
    if x == 0:
        print("The program have stopped!")
        break"""
    
    in_path = 'INPUT_' + str(x) + '.txt'

    # Check if input file exists
    if os.path.isfile(in_path): 
        W, m, w, v, c = loadInputFile(in_path)
        print("Reading data")
        print("Capacity: ", W)
        print("Number of classes: ", m)
        print("Weights: ", w)
        print("Values: ", v)

        # Solving knapsack problem
        max_value, taken = Knapsack(W, w, v, c, m)

        # Output the best profit
        print("\nFinal profit: ", max_value)
        print(c)
        print(taken)

        # Writing data to files
        out_path =  'OUTPUT_' + str(x) +  '.txt'
        with open(out_path, 'w') as fout:
            fout.write(str(max_value) + '\n')
            fout.write(', '.join(str(i) for i in taken))

        print("Successfully write data to output file!\n")
        break

    else: 
        print("Error! Input file does not exist.\n")
        continue

print("Program ends.")
