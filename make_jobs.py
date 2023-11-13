"""
f = open("LISA1mutationcellprio.txt", "r")
results = f.readlines()
f.close()

for x in range(10001):
    f = open("LISA1mutation20eval.txt", "a")
    f.write(results[x+20002])
    f.close()
"""

num = 25
print(num)
exp = 5
const = 10**-exp
print(num*const)
