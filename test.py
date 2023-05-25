import time

time_0 = time.time()

num = 0

for x in range(1000000000):
    num+=1

print(time.time() - time_0)