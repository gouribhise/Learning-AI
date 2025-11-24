#create line chart of random numbers

import matplotlib.pyplot as plt
import random

data=[random.randint(1,100) for _ in range(10)]

plt.plot(data)
plt.title("Line Chart Of Random Numbers")
plt.xlabel("Index")
plt.ylabel("Value")
plt.show()

#create a bar chart of 5 categories
categories=["A","B","C","D","E"]
values=[10,25,18,40,30]
plt.bar(categories,values)
plt.title("Bar Chart Of 5 Categories")
plt.xlabel("category")
plt.ylabel("value")
plt.show()