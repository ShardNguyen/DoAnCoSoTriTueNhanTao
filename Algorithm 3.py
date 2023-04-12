import random
import copy

# ---------- GLOBAL VARIABLES ---------
weightLimit = 20
itemList = []

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
def calculateHeuristic(flagList):
	totalWeight = 0
	totalValue = 0
	heuristic = 0
	bigNum = 0

	# Total weight = Total weight + item's weight * flag for item
	# Same for value
	for x in range(len(flagList)):
		bigNum += itemList[x].weight
		totalWeight += itemList[x].weight * flagList[x]
		totalValue += itemList[x].value * flagList[x]
	
	# When there is nothing in the bag
	if totalWeight == 0:
		for x in range(len(flagList)):
			heuristic += bigNum

	# Situations when the current state violate a restriction
	if totalWeight > weightLimit:
		heuristic += bigNum
	
	if totalValue != 0:
		heuristic += totalWeight / totalValue
	else:
		heuristic += bigNum

	return heuristic


# ----------- LOCAL BEAM SEARCH -----------
def localBeamSearch(flagList):
	kBest = 1			# Choose k best successors to expand
	bestSuccessor = copy.deepcopy(flagList)	# Initialize this with a list of 0s
	listOfSuccessors = []
	listOfStartSuccessors = []

	# Pick k random states to begin with (Ex: k = 1) and put them into listOfStartSuccesors
	for k in range(kBest):
		for x in range(len(flagList)):
			flagList[x] = random.randint(0, 1)
		listOfStartSuccessors.append(copy.deepcopy(flagList))

	print(listOfStartSuccessors)

	while 1:
		for k in range(kBest):
			# Next, expands the search list given the starting node and store them into another list
			# To do that, we need to make a copy of the list from the starting node
			tempFlagList = copy.deepcopy(listOfStartSuccessors[k])

			# Then extend the branch from the starting node (By flipping bit 1 by 1)
			for x in range(len(tempFlagList)):
				bit = tempFlagList[x]
				tempFlagList[x] = flipBit(bit)

				listOfSuccessors.append(copy.deepcopy(tempFlagList)) 	# Store the node into the list of successors

				tempFlagList[x] = bit # Return the flipped bit back to its original state
		
		# After getting all the successors, sort the list with heuristic going from low to high
		listOfSuccessors.sort(key=calculateHeuristic)
		# Then compare the best in the list with the best successor of all time
		if (calculateHeuristic(listOfSuccessors[0]) < calculateHeuristic(bestSuccessor)):
			bestSuccessor = copy.deepcopy(listOfSuccessors[0])

		# Clear the startSuccessors list and append top k
		listOfStartSuccessors.clear()
		for k in range(kBest):
			listOfStartSuccessors.append(copy.deepcopy(listOfSuccessors[k]))
		
		# Current goal: Find condition to break the while loop (Aka, finding the goal state)
		break

	# After the while loop, return the final result
	# print(listOfStartSuccessors)

def main():
	flagList = []
	listLength = 10

	for x in range(listLength):
		tempWeight = random.randint(1, 10)
		tempValue = random.randint(0, 100)
		tempType = random.randint(1, 3)
		i = item(tempWeight, tempValue, tempType)
		itemList.append(i)
		flagList.append(0)

	#for x in range(listLength):
	#	print(itemList[x], "\n")

	localBeamSearch(flagList)

main()
