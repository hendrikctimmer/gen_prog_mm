import time

time_0 = time.time()

x = 1
y = "h" + str(x)
print(y)

print("cast: ", time.time() - time_0)

time_0 = time.time()

x = 1
y = f"h{x}"
print(y)

print("no cast:", time.time() - time_0)