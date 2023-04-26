

class ItemList:
    value = []
    weight = []
    class_label = []
    m = 0
    def __init__(self, value, weight, class_label, m) -> None:
        self.value = value
        self.weight = weight
        self.class_label = class_label
        self.m = m


# return a list have 3 elements [totalValue, 
#                                list of 0 and 1 represent which item was choose, 
#                                bool satisfyTheConstraint]
def bruteForceSearching(WeightLimit, classHaveItem, itemList, n) -> []: 

    if n == 0:
        # the constraint(not exceed the weightLimt and each class have at least 1 items)
        if(WeightLimit >= 0 and classHaveItem == 2**itemList.m - 1): 
            return [0, [], True]
        else:
            return [0, [], False]
    # select this item
    WithItem = bruteForceSearching(WeightLimit - itemList.weight[n-1], classHaveItem | (1 << (itemList.class_label[n - 1] - 1)), itemList, n - 1)
    WithItem[0] += itemList.value[n-1]
    WithItem[1].insert(0, 1)


    #not select the item
    WithoutItem = bruteForceSearching(WeightLimit, classHaveItem, itemList, n - 1)
    WithoutItem[1].insert(0, 0)
    
    # both of them not satisfy the constraint -> no solution found
    if (WithItem[2] == False and WithoutItem[2] == False): 
        return [0, [], False]
    
    #one of them commit the rule return the other
    if(WithoutItem[2] == False): 
        return  WithItem
    if(WithItem[2] == False):
        return WithoutItem

    # 2 of them satisfy the rule, return the one who have higher totalValue
    if(WithoutItem[0] > WithItem[0]):
        return WithoutItem
    return WithItem

def bruteForceKnapsack(W, weights, values, class_label, num_of_class):
    itemList = ItemList(values, weights, class_label, num_of_class)
    max_profit, strItems, satisfyRule = bruteForceSearching(W, 0, itemList, len(values))
    if(satisfyRule == False): #commit the rule, the weight of each item exceed the max_weight or lack of classes
        return -1, []
    return max_profit, strItems