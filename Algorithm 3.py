import random

# Build class for items
class item:
	def __init__(self, value, type, weight):
		self.value = value
		self.type = type
		self.weight = weight

	def __str__(self):
		return f"Value: {self.value}, Type: {self.type}, Weight: {self.weight}"

# ----- NOTE -----
# Given the list with A items, create another list to flag if they're put into the bag or not

# Start with the simplest situation (k = 1, with only weight limit)
# Loop until restriction is reached

def localBeamSearch(flagForItemsPut, itemList):
	# Initialize some variables
	kBest = 1
	totalWeight = 0
	totalValue = 0

	# Pick a random item
	randomItem = random.randint(0, len(itemList) - 1)
	flagForItemsPut[randomItem] = 1
	totalWeight += itemList[randomItem].weight
	totalValue += itemList[randomItem].value

	# Next, find all of its successor (means try to combine with every other items)
	while 1:
		bestHeuristic = -1
		bestTotalWeight = totalWeight
		bestTotalValue = totalValue
		pickedItem = -1

		for x in range(len(itemList)):
			# If item is not listed, check
			if flagForItemsPut[x] == 0:
				# Else, start adding it up
				tempTotalWeight = totalWeight + itemList[x].weight
				tempTotalValue = totalValue + itemList[x].value

				# Then we compare with the best heuristic values
				# Check if tempHeuristic is used
				if bestHeuristic == -1:
					bestHeuristic = tempTotalWeight / tempTotalValue
					bestTotalWeight = tempTotalWeight
					bestTotalValue = tempTotalValue
					pickedItem = x
				else:
					currentItemHeuristic = tempTotalWeight / tempTotalValue
					if currentItemHeuristic < bestHeuristic:
						bestTotalWeight = tempTotalWeight
						bestTotalValue = tempTotalValue
						bestHeuristic = currentItemHeuristic
						pickedItem = x
		
		# Check conditions to break the while path
		# When no Item is picked
		if (pickedItem == -1):
			break
		
		# Else update flag list, totalWeight, totalValue
		flagForItemsPut[pickedItem] = 1
		totalWeight = bestTotalWeight
		totalValue = bestTotalValue

	print(flagForItemsPut)
	print(totalWeight, totalValue)

def main():
	itemList = []
	flagForItemPut = []

	for x in range(6):
		i = item(x + 8, x, x + 4)
		itemList.append(i)
		flagForItemPut.append(0)

	for x in range(6):
		print(itemList[x], "\n")

	localBeamSearch(flagForItemPut, itemList)

main()
