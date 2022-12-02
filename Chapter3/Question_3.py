"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 3 : Neural Decoding
Question 3
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# ============================================================================
# Imports
# ============================================================================
import numpy as np
import matplotlib.pyplot as plt
import random

# ============================================================================
# Set Parameters
# ============================================================================
trials = 1000                          # Number of Trials
teta = np.arange(-np.pi/2, np.pi/2, 0.01) # Wind direction
# Each neuron's prefered orientation (theta_i)
teta_i = [
    np.pi/4,
    3*np.pi/4,
    5*np.pi/4,
    7*np.pi/4
    ]

# ============================================================================
# Rates Calculation
# ============================================================================

# Rate array with 4 rows for each neuron and number of trials for each trial ..
# and also Third dim is for each teta
r = np.zeros((4, trials, np.shape(teta)[0]))
# Calculating rate for each trial j, teta t and teta_i i.
for j in range(trials):
    for t in range(np.shape(teta)[0]):
        for i in range(4):
            r[i, j, t] = (
                            (50 * np.cos(teta[t] - teta_i[i]))
                            + random.gauss(mu=0, sigma=5)
                            )
            if (r[i, j, t] < 0): r[i, j, t] = 0  

# ============================================================================
# Population vectors
# ============================================================================
x_i = np.zeros((4, trials, np.shape(teta)[0])) # X direction population vector
y_i = np.zeros((4, trials, np.shape(teta)[0])) # Y direction population vector

# Calculating x_i and y_i for each rial and each teta
for j in range(trials):
    for t in range(np.shape(teta)[0]):
        for i in range(4):
            x_i[i, j, t] = r[i, j, t] * np.cos(teta_i[i])
            y_i[i, j, t] = r[i, j, t] * np.sin(teta_i[i])

# Snumation of x_i and y_i to get population vectors X and Y
x = np.sum(x_i, axis=0, keepdims=True)
y = np.sum(y_i, axis=0, keepdims=True)
# Calculating estimated wind direction 
teta_est = np.arctan2(y, x)
# Calculating Error
se = (np.rad2deg(teta - teta_est)) ** 2 # Squered Error (converted to degrees)
mse = np.mean(se, axis=1)               # Mean-Squered-Error
rmse = np.sqrt(mse)                     # Root-Mean-Squered-Error
# Plot 
plt.plot(np.rad2deg(teta), rmse[0, :])
plt.xlabel('Wind Direction (degrees)')
plt.ylabel('Root-Mean-Squered-Error (degrees)')
plt.show()
