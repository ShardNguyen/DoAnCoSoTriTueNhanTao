from typing import List, Tuple
import os

# Global variables 
BB_solution = None
BB_stack = []
BB_tree = []

# READING DATA FROM FILES
def loadInputFile(input_file: str) -> Tuple[int, int, List[float], List[int], List[int]]:
    with open(input_file, 'r') as fin:
        W = float(fin.readline().strip())
        m = int(fin.readline().strip())
        w = list(map(float, fin.readline().strip().split(', ')))
        v = list(map(int, fin.readline().strip().split(', ')))
        c = list(map(int, fin.readline().strip().split(', ')))
    return W, m, w, v, c

# BINARY TREE 
class BTreeNode():
    def __init__(self):
        self.ParentNode = None
        self.Relaxation = 0
        self.Objective = 0
        self.ObjectID = -1
        self.Taken = None
        self.Room = None

# GETS BOUNDARY
def getBound(items, rootID, root_room, root_objective, weights, values, value_per_weight):
    while rootID < items and (root_room - weights[rootID + 1] >= 0):
        root_objective += values[rootID + 1]
        root_room -= weights[rootID + 1]
        rootID = rootID + 1
    
    if root_room > 0 and rootID < items:
        root_objective += min(root_room, weights[rootID + 1]) * value_per_weight[rootID + 1][1]

    return root_objective

# HANDLES ALL THE BRANCH LOGIC
def Branch(items, values, weights, value_per_weight):
    
    global BB_solution, BB_stack, BB_tree

    if not BB_stack:
        return 
    else:
        Root = BB_stack.pop()

    if BB_solution and Root.Relaxation < BB_solution.Objective:
        return 
    elif Root.ObjectID == items:
        return 
    
    Node = BTreeNode()
    Node.ObjectID = Root.ObjectID + 1
    Node.Room = Root.Room

    if Node.Room >= 0:
        Node.Objective = Root.Objective
        Node.Taken = 0
        Node.Relaxation = getBound(items, Node.ObjectID, Node.Room, Node.Objective, weights, values, value_per_weight)
        Node.ParentNode = Root
        BB_stack.append(Node)

        if Node.Objective == Node.Relaxation:
            if BB_solution and Node.Objective > BB_solution.Objective:
                BB_solution = Node
            elif BB_solution is None:
                BB_solution = Node
        
    BB_tree.append(Node)
    Node = BTreeNode()
    Node.ObjectID = Root.ObjectID + 1
    Node.Room = Root.Room - weights[Node.ObjectID]

    if Node.Room >= 0:
        Node.Objective = Root.Objective + values[Node.ObjectID]
        Node.Taken = 1
        Node.Relaxation = \
        getBound(items, Node.ObjectID, Node.Room, \
        Node.Objective, weights, values, value_per_weight)
        Node.ParentNode = Root
        BB_stack.append(Node)

        if Node.Objective == Node.Relaxation:
            if BB_solution and Node.Objective > BB_solution.Objective:
                BB_solution = Node
            elif BB_solution is None:
                BB_solution = Node

    BB_tree.append(Node)

# SOLVING KNAPSACK BRANCH AND BOUND
def Branch_And_Bound(capacity, weights, values, class_label, number_of_class):

    temp = values[:]

    global BB_tree, BB_stack # Array for indicating whether an element has been taken or not

    items = len(values) # Get number of items
    taken = [0] * items # Allocate memory for taking
    arr = []

    for index, value in enumerate(values):
        arr.append((index, value / weights[index], class_label[index]))
    
    # Sorts the list in descending order following the rule: value / weights
    arr.sort(key = lambda pair:pair[1], reverse = True)
    for i in range(1, number_of_class + 1):
        for j in arr:
            if i == j[2]:
                values[j[0]] = 9999999
                break

    value_per_weight = []

    for index, value in enumerate(values):
        value_per_weight.append((index, value / weights[index]))
    
    # Sorts the list in descending order
    value_per_weight.sort(key = lambda pair:pair[1], reverse = True)

    # Reorders the values and weights
    weights = [weights[element[0]] for element in value_per_weight]
    values = [values[element[0]] for element in value_per_weight]

    # Creates a root node
    Root = BTreeNode()
    Root.Room = capacity
    Root.Objective = 0
    Root.ObjectID = -1
    Root.Relaxation = getBound(items - 1, Root.ObjectID, Root.Room, Root.Objective, weights, values, value_per_weight)

    # Adds a root node to the tree
    BB_tree.append(Root)
    BB_stack.append(Root)

    # Branches while the stack is not empty
    while BB_stack:
        Branch(items - 1, values, weights, value_per_weight)

    # Retraces which items were taken and which were ignored
    Node = BB_solution

    while Node.ParentNode:
        taken[value_per_weight[Node.ObjectID][0]] = Node.Taken
        Node = Node.ParentNode

    maxValue = 0
    for i in range(len(temp)):
        if taken[i] == 1:
            maxValue += temp[i]

    return (maxValue, taken)

# MENU
x = -10

while x != 0:
    temp = input("Please input the sequence number of the test case (input 0 if you want to stop the program) \nx: ")

    # Incorrect input type (string, empty input, negative number, etc...)
    if temp.isnumeric() == False:
        print("Wrong input type! The input must be a positive number\n")
        continue
    
    x = int(temp)

    # Stop the program if the user enters 0
    if x == 0:
        print("The program have stopped!")
        break
    
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
        max_value, taken = Branch_And_Bound(W, w, v, c, m)

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

    else: 
        print("Error! Input file does not exist.\n")

print("Program ends.")





