import matplotlib.pyplot as plt
import numpy as np

#Data
density = np.array([ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
basic_agent = np.array([97.69, 90, 77, 71, 69, 65, 65, 63, 62])
improved_agent = np.array([100, 98, 86, 81, 79, 79, 75, 75, 71])

#plot lines
plt.plot(density, basic_agent, color="black")
plt.plot(density, improved_agent, color="red")

#plot dots
plt.scatter(density, basic_agent, color="black")
plt.scatter(density, improved_agent, color="red")

#label axis
plt.xlabel("Bomb Density")
plt.ylabel("Average Final Score")

#Display graph
plt.show()
