"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 14
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt

# --- Setting parameters ---
sigma_c = 0.3
sigma_s = 1.5
B = 5
K = np.arange(-10, 10, 0.1)        # Stimulus Spatial Frequency
x = np.arange(-2, 2, 0.1)       # X array
y = np.arange(-2, 2, 0.1)       # Y array

# --- Constructing stimulus S for each x and y and K ---
# Initializing Stimulus array 
S = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(K)[0]))
# Calculating stimulus S for each x and y and K
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        for n in range(np.shape(K)[0]):
            S[i, j, n] = np.cos(K[n] * x[i])

# --- Constructing kernel Ds (equation 2.45) ---
# Initializing Kernel array 
D = np.zeros((np.shape(x)[0], np.shape(y)[0]))
# Calculating kernel D for each x and y
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        D[i, j] = (
            ((1/(2*np.pi*(sigma_c**2))) * np.exp((x[i]**2 + y[j]**2)/(-2*(sigma_c**2))))
            - ((B/(2*np.pi*(sigma_s**2))) * np.exp((x[i]**2 + y[j]**2)/(-2*(sigma_s**2))))
        )

# --- Calculating spatial frequency tuning curve (by integral eq.(2.45) times stimulus)---
# Initializing tuning curve array T
T = np.zeros((np.shape(K)[0]))
# Calculating integral for each k
for i in range(np.shape(T)[0]):
    s = S[:, :, i]
    T[i] = np.sum(np.sum(s * D))
# Plot tuning curve
plt.plot(K, T)
plt.xlabel('K')
plt.ylabel('Amp')
plt.show()





