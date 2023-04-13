import random
import copy

# ---------- GLOBAL VARIABLES ---------
weightLimit = 20
typeAmount = 8
typeList = []
itemList = []
attemptLimit = 10
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
	# Special condition: value is 0
	if totalValue == 0:
		return bigNum * 3

	# When there is nothing in the bag
	if totalWeight == 0:
		heuristic += bigNum

	# Situations when the current state violate a restriction
	if totalWeight > weightLimit:
		heuristic += bigNum

	# Check how many type is left unchosen
	heuristic += len(tempRemainingTypeList)

	# Heuristic formula
	heuristic += 1  / totalValue 

	tempRemainingTypeList.clear()
	return heuristic


# ----------- LOCAL BEAM SEARCH -----------
def localBeamSearch():
	# Initialization
	kBest = 3			# Choose k best successors to expand
	attemptToFindBetterSuccessor = 0

	flagList = []
	for x in range(len(itemList)):
		flagList.append(0)

	bestSuccessor = copy.deepcopy(flagList)	# Initialize this with a list of 0s
	listOfSuccessors = []
	listOfStartSuccessors = []

	# Pick k random states to begin with (Ex: k = 1) and put them into listOfStartSuccesors
	for k in range(kBest):
		for x in range(len(flagList)):
			flagList[x] = random.randint(0, 1)
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
		
		# After getting all the successors, sort the list with heuristic going from low to high
		listOfSuccessors.sort(key=calculateHeuristic)
		# Then compare the best in the list with the best successor of all time
		if (calculateHeuristic(listOfSuccessors[0]) < calculateHeuristic(bestSuccessor)):
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

def main():
	listLength = 10

	# Create an empty type list
	for x in range(typeAmount):
		typeList.append(0)

	for x in range(listLength):
		tempWeight = random.randint(1, 10)
		tempValue = random.randint(0, 100)
		tempType = random.randint(1, typeAmount)
		i = item(tempWeight, tempValue, tempType)

		itemList.append(i)
		typeList[tempType - 1] = tempType	# Track which types of item is inside the item list

	while (typeList.count(0)):	# Clear out any types that doesn't have an item inside the itemList
		typeList.remove(0)

	for x in range(listLength):
		print(itemList[x], "\n")

	result = localBeamSearch()
	print(result)

main()
