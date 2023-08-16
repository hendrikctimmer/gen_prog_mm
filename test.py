import time

time_0 = time.time()

num = 1

for x in range(100000000):
    num +=1

print("time: ", time.time() - time_0)
print(num)