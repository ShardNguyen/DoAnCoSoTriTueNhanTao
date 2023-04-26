import random
import copy

# ---------- CLASSES ----------
class item:
    def __init__(self, weight, value, type):
        self.weight = weight
        self.value = value
        self.type = type

    def __str__(self):
        return f"Value: {self.value}, Type: {self.type}, Weight: {self.weight}"

# ---------- ADDITIONAL FUNCTIONS ----------
def flipBit(bit):
    if bit == 1:
        return 0
    elif bit == 0:
        return 1
    else: # Return error if bit is not 0 or 1
        return -1

# Need adjustment
def calculateHeuristic(flagList, weightLimit, itemList, typeList):
    totalWeight = 0
    totalValue = 0
    heuristic = 0
    bigNum = 2 + len(flagList)
    tempRemainingTypeList = copy.deepcopy(typeList)

    # Check how many types are left unchosen
    # Calculate totalWeight and totalValue
    for x in range(len(flagList)):
        # Check if item is chosen
        if (flagList[x] == 1):
            # Check if the type is chosen in the list (count = 0 means chosen)
            if (tempRemainingTypeList.count(itemList[x].type)):
                tempRemainingTypeList.remove(itemList[x].type)
            totalWeight += itemList[x].weight
            totalValue += itemList[x].value

    # This is for restrictions
    # Special condition: Value = 0 or Weight = 0
    if totalValue == 0 or totalWeight == 0:
        return bigNum * 3

    # Check if the bag is violating the weightLimit
    if totalWeight > weightLimit:
        heuristic += bigNum + (totalWeight - weightLimit)

    # Check how many type is left unchosen
    heuristic += len(tempRemainingTypeList)

    # Heuristic formula
    heuristic += 1  / totalValue

    tempRemainingTypeList.clear()
    return heuristic


# ----------- LOCAL BEAM SEARCH -----------
def localBeamSearch(itemList, weightLimit, typeList, attemptLimit):
    # Initialization
    kBest = 5		# Choose k best successors to expand
    attemptToFindBetterSuccessor = 0

    flagList = []
    for x in range(len(itemList)):
        flagList.append(0)

    bestSuccessor = copy.deepcopy(flagList)	# Initialize this with a list of 0s
    listOfSuccessors = []
    listOfStartSuccessors = []

    # Pick k random states to begin with (Ex: k = 1) and put them into listOfStartSuccesors
    listOfStartSuccessors.append([0]*len(itemList))
    for k in range(kBest - 1):
        totalWeight = 0
        for x in range(len(flagList)):
            if(totalWeight < weightLimit):
                flagList[x] = random.randint(0, 1)
            else: #if 
                flagList[x] = random.choices([0,1], weights = [1000, 1], k = 1)[0]
            
            if(flagList[x] == 1):
                totalWeight += itemList[x].weight
            
        listOfStartSuccessors.append(copy.deepcopy(flagList))

    while 1:
        attemptToFindBetterSuccessor += 1
        
        for k in range(kBest):
            # Next, expands the search list given the starting node and store them into another list
            # To do that, we need to make a copy of the list from the starting node
            tempFlagList = copy.deepcopy(listOfStartSuccessors[k])

            # Then extend the branch from the starting node (By flipping bit 1 by 1)
            for x in range(len(flagList)):
                bit = tempFlagList[x]
                tempFlagList[x] = flipBit(bit)
                listOfSuccessors.append(copy.deepcopy(tempFlagList)) 	# Store the node into the list of successors
                tempFlagList[x] = bit # Return the flipped bit back to its original state
    
        def getHeuristic(Successors):
            return calculateHeuristic(Successors, weightLimit, itemList, typeList)

        # After getting all the successors, sort the list with heuristic going from low to high
        listOfSuccessors.sort(key=getHeuristic)
        # Then compare the best in the list with the best successor of all time
        if (getHeuristic(listOfSuccessors[0]) < getHeuristic(bestSuccessor)):
            bestSuccessor = copy.deepcopy(listOfSuccessors[0])
            attemptToFindBetterSuccessor = 0

        # Clear the startSuccessors list and append top k
        listOfStartSuccessors.clear()
        for k in range(kBest):
            listOfStartSuccessors.append(copy.deepcopy(listOfSuccessors[k]))

        #Finally clear the list of Successors
        listOfSuccessors.clear()

        if attemptToFindBetterSuccessor >= attemptLimit:
            break

    return bestSuccessor

def localBeamKnapsack(W, weights, values, class_label, num_of_class):
    
    #attempt to go more 10 nodes since it find the current max, if cannot find any better solution then return
    attemptLimit = 20
    weightLimit = W
    listLength = len(values)
    typeAmount = 10
    
    typeList = []
    itemList = []

    # Create an empty type list
    for x in range(num_of_class):
        typeList.append(0)

    for x in range(listLength):
        i = item(weights[x], values[x], class_label[x])

        itemList.append(i)
        typeList[class_label[x] - 1] = class_label[x]	# Track which types of item is inside the item list


    result = localBeamSearch(itemList, weightLimit, typeList, attemptLimit)
    
    # Check if the result violates any restrictions
    # If the heuristic is <= 1, it means the solution satisfy the constraint
    if calculateHeuristic(result, weightLimit, itemList, typeList) <= 1:
        totalVal = 0
        for i in range(len(result)):
            if(result[i] == 1):
                totalVal += values[i]
        return totalVal, result
    else:
        return -1, [] #cannot find the solution

