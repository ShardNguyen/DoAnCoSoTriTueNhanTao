

class ItemList:
    value = []
    weight = []
    group = []
    m = 0
    n = 0
    def __init__(self, value, weight, group, m, n) -> None:
        self.value = value
        self.weight = weight
        self.group = group
        self.m = m
        self.n = n


def bruteForceKnapsack(W, itemList):
    res = bruteForceSearching(W, 0, itemList, itemList.n)
    sol = []
    for i in range(0, itemList.n):
        if i in res[1]:
            sol.append(1)
        else:
            sol.append(0)
    return res[0], sol
    
def bruteForceSearching(W, classHaveItem, itemList, n) :
    if n == 0 or W == 0:

        return [0, [], classHaveItem == 2**itemList.m - 1]

    if itemList.weight[n-1] > W :
        return bruteForceSearching(W, classHaveItem, itemList, n - 1)
    else:
        NotSelectItem = bruteForceSearching(W, classHaveItem, itemList, n - 1)

        # select this item
        SelectItem = bruteForceSearching(W - itemList.weight[n-1], classHaveItem | (1 << (itemList.group[n - 1] - 1)), itemList, n - 1)
        SelectItem[0] += itemList.value[n-1]
        SelectItem[1].append(n - 1)

        if (SelectItem[2] == False and NotSelectItem[2] == False):
            return [-1, [], False]
        if(NotSelectItem[2] == False):
            return  SelectItem
        if(SelectItem[2] == False):
            return NotSelectItem

        if(NotSelectItem[0] > SelectItem[0]):
            return NotSelectItem
        return SelectItem
        
W = 101
itemWeight = [85, 26, 48, 21, 22, 95, 43, 45, 55, 52]
itemValue = [79, 32, 47, 18, 26, 85, 33, 40, 45, 59]
itemClass = [1, 1, 2, 1, 2, 1, 1, 2, 2, 2]
n = 10

itemList = ItemList(itemValue, itemWeight, itemClass, 2, 10)

maxProfit, sol = bruteForceKnapsack(W,itemList)
print(maxProfit)
print(sol)