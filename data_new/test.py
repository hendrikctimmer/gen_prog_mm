import matplotlib.pyplot as plt
import numpy as np
import statistics
import pandas as pd
from scipy.optimize import curve_fit

data_1 = [1,2,3,4,5,6,7,8,9,10]
data_2 = [1,2,3,4,5,6,7,8,9,10]
dataz = [data_1,data_2]

df = pd.DataFrame(data=dataz)

print(df)
print(max(data_1))