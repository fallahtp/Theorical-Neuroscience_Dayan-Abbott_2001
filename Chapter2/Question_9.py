"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 9
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

# ---Set Parameters ---
alpha = (1/15) * 1e3                # Parameter for Kernel D, eq.(2.29)
omega = 6*np.pi                     # Stimulus temporal frequency
dt = 1e-3                           # Time step
t = np.arange(0, 1, dt)             # Time array
tau = np.arange(0, 0.3, dt)         # Tau array for calculating D

# --- Calculating kernel D and stimulus S ---
D = alpha * np.exp(-alpha*tau) * (((alpha*tau) ** 5) / factorial(5) - ((alpha*tau) ** 7) / factorial(7))   # Kernel D, according to eq.(2.29)
S = np.cos(omega*t)                                                                                        # Stimulus S 

# --- Calculating response L ---
L = np.zeros(np.shape(t))                # Initializing array L to calculate response in the following loop
for i in range(np.shape(t)[0]):          # Loop through each time point and calculating L
    if i < np.shape(D)[0]:               # The case that t is less than size of our kernel so we should cut D to avoid (t-tau) < 0
        d = np.flip(D[0:i])              # Cut D to the size of our S in the current time point
        s = S[0:i]                       # Stimulus from the bigining to this time point
        L[i] = np.sum(d*s)               # Calculating response according to eq.(2.32)
    elif i>= np.shape(D)[0]:
        s    = S[i-np.shape(D)[0]: i]    # Cut stimulus from tau ms before the current time point until the current time point
        L[i] = np.sum(np.flip(D)*s)      # Calculating response according to eq.(2.32)

# --- Plots ---
plt.figure()                    # Plot Stimulus
plt.plot(t, S)
plt.xlabel('Time [Second]')
plt.ylabel('Stimulus')
plt.title('Stimulus')

plt.figure()                    # Plot simple cell response
plt.plot(t, L)
plt.xlabel('Time [Second]')
plt.ylabel('L')
plt.title('Simple Cell')

plt.figure()                    # Plot complex cell response
plt.plot(t, L**2)
plt.xlabel('Time [Second]')
plt.ylabel('L^2')
plt.title('Complex Cell')

plt.show()


