import random

# Build class for items
class item:
	def __init__(self, weight, value, type):
		self.weight = weight
		self.value = value
		self.type = type

	def __str__(self):
		return f"Value: {self.value}, Type: {self.type}, Weight: {self.weight}"

def flipBit(bit):
	if bit == 1:
		bit = 0
	elif bit != 0:
		bit = 1
	else: # Return error if bit is not 0 or 1
		bit = -1

def calculateHeuristic(tempFlagList, itemList, weightLimit):
	totalWeight = 0
	totalValue = 0
	heuristic = 0

	# Total weight = Total weight + item's weight * flag for item
	# Same for value
	for x in range(len(tempFlagList)):
		totalWeight += itemList[x].weight * tempFlagList[x]
		totalValue += itemList[x].value * tempFlagList[x]
	
	# When there is nothing in the bag
	if totalWeight == 0:
		heuristic = 10000
	# Situations when the current state violate a restriction
	if totalWeight > weightLimit:
		heuristic = 10000

	heuristic += totalWeight / totalValue
	return heuristic


def localBeamSearch(flagForItemsPut, itemList, weightLimit):
	kBest = 1			# Choose k best successors to expand 

	# Pick a random state to begin with (For example: 10010110)
	for x in range(len(flagForItemsPut)):
		flagForItemsPut[x] = random.randit(0, 1)

	# Store temp flag list for comparision
	tempFlagList = flagForItemsPut

	# Next, find all of its successor (Flips one bit at a time) and finds the best heuristic
	while 1:
		currentBestHeuristic = -1	# Save the best heuristic
		indexForBestHeuristic = -1	# Save the index of the item that leads to best heuristic

		for x in range(len(flagForItemsPut)):
			flipBit(tempFlagList[x])	# Flip a bit
			currentHeuristic = calculateHeuristic(tempFlagList, itemList, weightLimit)
			
			if currentBestHeuristic == -1 or currentHeuristic < currentBestHeuristic:
				currentBestHeuristic = currentHeuristic
				indexForBestHeuristic = x

			flipBit(tempFlagList[x])	# Return back to temp's initial state

		flipBit(tempFlagList[indexForBestHeuristic])	# Flip the bit that returns the best heuristic

	# After the while loop, return the final result
	flagForItemsPut = tempFlagList
	print(flagForItemsPut)

def main():
	itemList = []
	flagForItemPut = []
	weightLimit = 20
	listLength = 10

	for x in range(listLength):
		tempWeight = random.randint(1, 10)
		tempValue = random.randint(0, 100)
		tempType = random.randint(1, 3)
		i = item(tempWeight, tempValue, tempType)
		itemList.append(i)
		flagForItemPut.append(0)

	for x in range(listLength):
		print(itemList[x], "\n")

	localBeamSearch(flagForItemPut, itemList, weightLimit)

main()
