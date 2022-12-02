"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 8
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt

# ---Set Parameters ---
THETA   = 0                                # Stimulus Orientation
PHI     = 0                                # Stimulus Spatial Phase
A       = 5                                # Stimulus Amplitude
K       = np.arange(0, 6, 0.01)            # Stimulus Spatial Frequency
sigma   = 1                                # Represent Extention of Gabor Kernel in x and y direction
phi_1   = 0                                # Prefered Spatial Phase of the Gabor Kernel D_1
phi_2   = -np.pi/2                         # Prefered Spatial Phase of the Gabor Kernel D_2
k       = 2                                # Prefered Spatial Frequency of the Gabor Kernel D
x       = np.arange(-5, 5, 0.1)            # X array
y       = np.arange(-5, 5, 0.1)            # Y array

# --- Computing Stimulus S(x, y) And Kernel D1(x, y) and D2(x, y) For Different Values of Stimulus Spatial Frequency K ---
S = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(K)[0]))                                                              # Initializing Stimulus Array (third dimension is used for different values of K) 
for n in range(np.shape(K)[0]):                                                                                             # Loop through different values of K         
    for i in range(np.shape(x)[0]):                                                                                         # Loop for each x point
        for j in range(np.shape(y)[0]):                                                                                     # Loop for each y point
            S[i, j, n] = A * np.cos(K[n]*x[i]*np.cos(THETA) + K[n]*y[j]*np.sin(THETA) - PHI)                                # Calculating Stimulus S for corresponding x, y and K

D_1 = np.zeros((np.shape(x)[0], np.shape(y)[0]))                                                                            # Initializind array D_1 for calculating Kernel D1
D_2 = np.zeros((np.shape(x)[0], np.shape(y)[0]))                                                                            # Initializind array D_2 for calculating Kernel D2
for i in range(np.shape(x)[0]):                                                                                             # Loop for each x point
    for j in range(np.shape(y)[0]):                                                                                         # Loop for each y point
        D_1[i, j] = (1/(2*np.pi*(sigma**2))) * (np.exp(-(x[i]**2 + y[j]**2) / (2*(sigma**2)))) * np.cos(k*x[i] - phi_1)     # Calculating Gabor kernel D for each x and y
        D_2[i, j] = (1/(2*np.pi*(sigma**2))) * (np.exp(-(x[i]**2 + y[j]**2) / (2*(sigma**2)))) * np.cos(k*x[i] - phi_2)     # Calculating Gabor kernel D for each x and y

L_1 = np.zeros((np.shape(K)[0]))                                                                                            # Initalizing L_1 array for spatial Response for each K
L_2 = np.zeros((np.shape(K)[0]))                                                                                            # Initalizing L_2 array for spatial Response for each K
for i in range(np.shape(L_1)[0]):                                                                                           # Loop for different values of K
    s      = S[:, :, i]                                                                                                     # Corresponding stimulus for given K
    L_1[i] = (np.sum(np.sum(s * D_1))) ** 2                                                                                 # Calculating L1^2 according to equation (2.31)
    L_2[i] = (np.sum(np.sum(s * D_2))) ** 2                                                                                 # Calculating L2^2 according to equation (2.31)
plt.plot(K/k, L_1 + L_2)                                                                                                    # Plot L_s for different values of K/k
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

L_1 = np.zeros((np.shape(PHI)[0]))                                                                                      # Initalizing L_1 array for spatial Response for each PHI
L_2 = np.zeros((np.shape(PHI)[0]))                                                                                      # Initalizing L_2 array for spatial Response for each PHI
for i in range(np.shape(L_1)[0]):                                                                                       # Loop for different values of PHI
    s      = S[:, :, i]                                                                                                 # Corresponding stimulus for given PHI
    L_1[i] = (np.sum(np.sum(s * D_1)))                                                                                  # Calculating L1^2 according to equation (2.31)
    L_2[i] = (np.sum(np.sum(s * D_2)))                                                                                  # Calculating L2^2 according to equation (2.31)

plt.figure()                                                                                                            # Plot L_s for different values of PHI
plt.plot(PHI, L_1**2 , 'blue')
plt.plot(PHI, L_2**2, 'red')
plt.plot(PHI, L_2**2 + L_1**2, 'green')
plt.xlabel('\u03A6')
plt.legend(['L_1^2', 'L_2^2', 'L_1^2 + L_1^2'])

plt.show()





