from collections import deque
from typing import List, Tuple


# DEFINE AN ITEM
class Item:
    def __init__(self, weight: int, value: int, class_label: int, first_index: int):
        self.weight = weight
        self.value = value
        self.ratio = value / weight
        self.class_label = class_label
        self.first_index = first_index # Store the bit to represent if the item is put in the bag or not (0: not taken, 1: taken)

# DEFINE AN ITEM AS A NODE IN A BINARY TREE
class KnapsackNode:
    def __init__(self, weight: int, profit: int, level: int, bound: int, class_select: int, choose: str):
        self.weight = weight
        self.profit = profit
        self.level = level
        self.bound = bound
        self.class_select = class_select # Count how many class has been selected 
        self.choose = choose # Store the string represent the number of class has been taken (Ex: 0 1 0 means that in the bag there are only items of class 2 but no items of class 1 and 3)

# GET THE BOUND FOR EACH NODE
def getBound(Node, n, W, Item_list, m):

    # If the weight while solving in a case is larger than W then eliminate this case
    if Node.weight >= W:
        return 0
    
    check_class = Node.class_select
    # Move to the next node
    next_level = Node.level + 1

    # Using bits shift left and bitwise OR (|) to update the string containing which class has been included
    while (next_level < n):
        check_class |= (1 << (Item_list[next_level].class_label - 1)) 
        next_level += 1 # Move to the next node
    
    # If the total class of all items in the case that is being checked is not enough, eliminate that case as well
    if (2**m - 1 != check_class):
        return 0

    profit_bound = Node.profit

    j = Node.level + 1 # Move to the next node
    totalWeight = Node.weight

    # Continue checking when the level of a node has not reached the end (meaning there are items can be put in the bag) and the total weight has not exceeded W
    while (j < n) and (totalWeight + Item_list[j].weight <= W):
        totalWeight += Item_list[j].weight # Update the total weight
        profit_bound += Item_list[j].value # Update the max profit
        j += 1 # Move to the next node
    
    if j < n:
        profit_bound += (W - totalWeight) * Item_list[j].value / Item_list[j].weight

    return profit_bound

# SOLVING THE KNAPSACK PROBLEM
def BranchAndBoundKnapsack(W, weights, values, class_label, num_of_class):
    
    # List containing all the items
    Item_list = []

    # Appending each item into the list
    for index, value in enumerate(values):
        Item_list.append(Item(weights[index], values[index], class_label[index], index))

    # Sorting the list in order value per weight descending using the ratio already implemented in each item
    Item_list.sort(key = lambda x:x.ratio, reverse=True)

    # Using a stack to store qualified items 
    stack = deque()
    stack.append(KnapsackNode(0, 0, -1, -1, 0, ''))
    n = len(values)  # Get the number of items
    maxProfit = 0    # The maximum value we can get from a list of items
    best_string = '' # Store the string contains only number 0 or 1, representing each item in the list is chosen or not 

    # Solving
    while stack:
        u = stack.pop() # Using a stack to implement DFS for solving
        
        if u.level == n-1: # Return when reaching a leaf node
            continue

        nextLevel = u.level + 1  # Get the level of the next node
        
        # Eliminate the item that is not satisfied
        withoutItem = KnapsackNode(u.weight, u.profit, nextLevel, 0, u.class_select, '')
        withoutItem.bound = getBound(withoutItem, n, W, Item_list, num_of_class)
        withoutItem.choose = u.choose + '0'
        
        if withoutItem.bound > maxProfit:
            stack.append(withoutItem)
            
        # Choose the item that is satisfied
        withItem = KnapsackNode(u.weight + Item_list[nextLevel].weight, u.profit + Item_list[nextLevel].value, nextLevel, 0, u.class_select | (1 << (Item_list[nextLevel].class_label - 1)), '')
        withItem.bound = getBound(withItem, n, W, Item_list, num_of_class)
        withItem.choose = u.choose + '1'

        # If the item is chosen, update the profit and the string 
        if (withItem.weight <= W and withItem.profit > maxProfit and (2**num_of_class - 1 == withItem.class_select)):
            maxProfit = withItem.profit
            best_string = withItem.choose

        if withItem.bound > maxProfit:
            stack.append(withItem)
    

    if(maxProfit == 0): #cannot find the solution, maybe the weight of each item exceed the max_weight or lack of classes
        return -1, []
    # Create a string to store a list of items that is chosen or not and represent it as 0 or 1       
    bestString = []
    for i in range(0, n):
        bestString.append(0)

    for i in range(0, len(best_string)):
        if best_string[i] == '1':
            bestString[Item_list[i].first_index] = 1
        
    return maxProfit, bestString
