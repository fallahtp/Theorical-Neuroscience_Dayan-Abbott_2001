"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 12
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

# --- Setting parameters ---
omega = 8*np.pi                 # Stimulus temporal frequency
dt = 1e-3                       # Time step
t = np.arange(0, 1, dt)         # Time array
tau = np.arange(0, 0.3, dt)     # Tau array for calculating D
x = np.arange(-2, 2, 0.1)       # X array
y = np.arange(-2, 2, 0.1)       # Y array
c = 0.02 * 1e3                  # Conversion factor eq.(2.36) and eq.(2.37)
si = np.pi/9                    # rotatin angle eq.(2.36) and eq.(2.37)
K = np.arange(-np.pi, np.pi, 0.5)   # Stimulus Spatial Frequency
sigma = 1                       # Represent Extention of Kernel D_s in x and y direction
phi = 0                         # Prefered Spatial Phase of the Gabor Kernel D_s
k = 2                           # Prefered Spatial Frequency of the Gabor Kernel D_s
alpha = 20 * 1e-3               # Parameter for Kernel D, eq.(2.29)

# --- Constructing Stimulus ---
# Initializing stimulus array S
S = np.zeros((np.shape(K)[0], np.shape(x)[0], np.shape(y)[0], np.shape(t)[0]))
# Calculating stimulus for each time point n and each x and y and each K o
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        for n in range(np.shape(t)[0]):
            for o in range(np.shape(K)[0]):
                S[o, i, j, n] = np.cos(K[o]*x[i] - omega*t[n])

# --- Constructing Kernel D(x, y, tau) ---
# Initializing Kernel D(x, y, tau)
D = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(tau)[0]))
# Calculating D_s(x, y) for each x and y (equation 2.27)
for o in range(np.shape(tau)[0]):
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(y)[0]):
            x_p = x[i]*np.cos(si) - c*tau[o]*np.sin(si)
            tau_p = tau[o]*np.cos(si) + (x[i]/c)*np.sin(si)
            D_s = ((1 / (2*np.pi*sigma))
                    * (np.exp((-x_p**2 - y[j]**2)/(2*sigma**2)))
                    * (np.cos(k*x_p - phi)))
            D_t = (
                alpha
                * np.exp(-alpha*tau_p)
                * (((alpha*tau_p)**5)/factorial(5))
                )
            D[i, j, o] = D_s * D_t
# --- Calculating the linear estimate of response (as a function of time) ---
# Initializing estimated response array each row for one K
L = np.zeros((np.shape(K)[0], np.shape(t)[0]))
for i in range(np.shape(L)[0]):
    for j in range(np.shape(L)[1]):
        if j < np.shape(tau)[0]:
            s = S[i, :, :, 0:j]
            d = D[:, :, 0:j]
            s = s[:, :, ::-1]   # Fliping
            L[i, j] = np.sum(np.sum(d*s))
        else:
            s = S[i, :, :, j-np.shape(tau)[0]:j]
            s = s[:, :, ::-1]   # Fliping
            L[i, j] = np.sum(np.sum(D*s))

# --- Plot ---
plt.plot(K, np.amax(L, axis=1))
plt.xlabel('K')
plt.ylabel('Max Amplitude')
plt.show()

