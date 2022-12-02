"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 7
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt

# ---Set Parameters ---
THETA = 0                            # Stimulus Orientation
PHI   = 0                            # Stimulus Spatial Phase
A     = 50                           # Stimulus Amplitude
K     = np.arange(0, 6, 0.01)        # Stimulus Spatial Frequency
sigma = 1                            # Represent Extention of Gabor Kernel in x and y direction
phi   = 0                            # Prefered Spatial Phase of the Gabor Kernel D
k     = 2                            # Prefered Spatial Frequency of the Gabor Kernel D
x = np.arange(-5, 5, 0.1)            # X array
y = np.arange(-5, 5, 0.1)            # Y array

# --- Computing Stimulus S(x, y) And Kernel D(x, y) For Different Values of Stimulus Spatial Frequency K ---
S = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(K)[0]))                                                          # Initializing Stimulus Array (third dimension is used for different values of K) 
for n in range(np.shape(K)[0]):                                                                                         # Loop through different values of K         
    for i in range(np.shape(x)[0]):                                                                                     # Loop for each x point
        for j in range(np.shape(y)[0]):                                                                                 # Loop for each y point
            S[i, j, n] = A * np.cos(K[n]*x[i]*np.cos(THETA) + K[n]*y[j]*np.sin(THETA) - PHI)                            # Calculating Stimulus S for corresponding x, y and K

D = np.zeros((np.shape(x)[0], np.shape(y)[0]))                                                                          # Initializind array D for calculating Kernel D
for i in range(np.shape(x)[0]):                                                                                         # Loop for each x point
    for j in range(np.shape(y)[0]):                                                                                     # Loop for each y point
        D[i, j] = (1/(2*np.pi*(sigma**2))) * (np.exp(-(x[i]**2 + y[j]**2) / (2*(sigma**2)))) * np.cos(k*x[i] - phi)     # Calculating Gabor kernel D for each x and y

L = np.zeros((np.shape(K)[0]))                                                                                          # Initalizing L array for spatial Response for each K
for i in range(np.shape(L)[0]):                                                                                         # Loop for different values of K
    s    = S[:, :, i]                                                                                                   # Corresponding stimulus for given K
    L[i] = np.sum(np.sum(s * D))                                                                                        # Calculating L according to equation (2.31)

plt.plot(K/k, L)                                                                                                        # Plot L_s for different values of K/k
plt.xlabel('K/k')
plt.ylabel('L_s')

# --- Calculating Stimulus for different values of PHI ---
K   = 2                                                                                                                 # Stimulus Spatial Frequency
PHI = np.arange(-2.5, 2.5, 0.1)                                                                                         # Stimulus Spatial Phase
S   = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(PHI)[0]))                                                      # Initializing Stimulus Array (third dimension is used for different values of PHI)
for n in range(np.shape(PHI)[0]):                                                                                       # Loop through different values of K
    for i in range(np.shape(x)[0]):                                                                                     # Loop for each x point
        for j in range(np.shape(y)[0]):                                                                                 # Loop for each y point
            S[i, j, n] = A * np.cos(K*x[i]*np.cos(THETA) + K*y[j]*np.sin(THETA) - PHI[n])                               # Calculating Stimulus S for corresponding x, y and PHI

L = np.zeros((np.shape(PHI)[0]))                                                                                        # Initalizing L array for spatial Response for each PHI  
for i in range(np.shape(L)[0]):                                                                                         # Loop for different values of PHI
    s    = S[:, :, i]                                                                                                   # Corresponding stimulus for given PHI
    L[i] = np.sum(np.sum(s * D))                                                                                        # Calculating L according to equation (2.31)

plt.figure()                                                                                                            # Plot L_s for different values of PHI
plt.plot(PHI, L)
plt.xlabel('\u03A6')
plt.ylabel('L_s')

plt.show()



