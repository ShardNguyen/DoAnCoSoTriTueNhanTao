# Phu Thanh Nhan
# 21127382

# Packages
import random as rng  # For RNG
import numpy as np  # For arrays

# end


# function
def percent(part, whole):
    return (part * whole) / 100.0


# end

i = rng.randint(1, 3)  # How many items are there
W = rng.randint(100, 1000)  # Knapsack capacity

m = rng.randint(1, 4)  # Number of classes

value_range = range(1, W)  # Need to use value_range to remove the chance of duplicating weight but different value
Wi = rng.sample(value_range, (10 - i))  # Weights


vi = np.empty(10 - i, dtype=object)
for x in range(10 - i):
    vi[x] = np.random.randint(Wi[x] - int(percent(Wi[x], 10)), Wi[x] + int(percent(Wi[x], 10))) # Values

ci = np.random.randint(1, m + 1, 10 - i)  # Correspond classes


file = open("Input.txt", "w")
# Open file under 'w' write mode

file.write(repr(W) + "\n")
file.write(repr(m) + "\n")

a = 0
for x in Wi:
    file.write(repr(x))
    if a >= (len(Wi) - 1):
        break
    file.write(", ")
    a += 1

file.write("\n")

a = 0
for x in vi:
    file.write(repr(x))
    if a >= (len(vi) - 1):
        break
    file.write(", ")
    a += 1
file.write("\n")

a = 0
for x in ci:
    file.write(repr(x))
    if a >= (len(ci) - 1):
        break
    file.write(", ")
    a += 1
file.write("\n")


file.close()
# Close the file
