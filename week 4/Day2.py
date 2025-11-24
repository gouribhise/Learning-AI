#Visualize token count,time count and word frequency

import matplotlib.pyplot as plt
from collections import Counter



token_usage=[120,95,140,200,160]
plt.plot(token_usage)
plt.title("Token Count Per AI Request")
plt.xlabel("Request Number")
plt.ylabel("Tokens")
plt.show()

times=[0.8,1.2,0.9,1.5,1.1]

plt.bar(range(len(times)),times)
plt.title("Time Taken Per Request")
plt.xlabel("Request Number")
plt.ylabel("Seconds")
plt.show()


text="AI makes life easy because AI makes automate tasks"
words=text.lower().split()
freq=Counter(words)

plt.bar(freq.keys(),freq.values())
plt.title("Word Frequency")
plt.xticks(rotation=45)
plt.show()
