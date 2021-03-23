import matplotlib.pyplot as plt
import numpy as np

#Data
density = np.array([ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
basic_agent = np.array([ (11/26)*100, (18/51)*100, (22/77)*100, (29/102)*100, (43/128)*100, (54/154)*100, (77/179)*100, (112/205)*100, (156/230)*100])
improved_agent = np.array([ (25/26)*100,  (45/51)*100, (55/77)*100, (60/102)*100, (68/128)*100, (77/154)*100, (109/179)*100, (148/205)*100, (187/230)*100])

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
