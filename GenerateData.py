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

n = 1000 # How many items are there
W = rng.randint(100, n*50)  + rng.randint(0,99) / 100# Knapsack capacity

m = rng.randint(2, 10)  # Number of classes
Wi = []
for i in range(n):
    weight = rng.randint(1, int(W/2)) + rng.randint(0, 99) /100 #floating point number truncated to 2 decimal places
    Wi.append(weight) # Weights


vi = np.empty(n, dtype=object)
for x in range(n):
    vi[x] = np.random.randint(Wi[x] - int(percent(Wi[x], 10)) - 1, Wi[x] + int(percent(Wi[x], 10))) # Values
# I need to add -1 to the Wi[x] - due to in rare circumstances it will result in low >= high

ci_temp = []
for x in range(1, m + 1):
    ci_temp += [x]
unique_values = set(ci_temp)

ci = []
for x in unique_values:
    ci.append(x)

rng.shuffle(ci)

while len(ci) < n:
    random_value = rng.choice(ci_temp)
    ci.append(random_value)

rng.shuffle(ci) # Correspond classes


inpath = 'INPUT/INPUT_' + str(10) + '.txt'
file = open(inpath, "w")
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