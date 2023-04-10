import random

# Step 1: Build every classes possible
class items:
	def __init__(self, value, type, weight):
		self.value = value
		self.type = type
		self.weight = weight

def getHeuristic(item):
	return item.heuristic

# ---------------------------------------
# Step 2: Implement the Local Beam Search

def localBeamSearch(itemList):
	# Initialize
	bestAmountOfSuccessors = 2

	# Pick a random start node
	startIndex = random.randint(0, len(itemList) - 1)
	startNode = itemList[startNode]

	# Pick random states from start node (Just pick the next nodes)
	
