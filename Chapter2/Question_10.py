"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 10
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
sigma = 1   # Represent Extention of Kernel D_s in x and y direction
phi = 0   # Prefered Spatial Phase of the Gabor Kernel D_s
k = 2       # Prefered Spatial Frequency of the Gabor Kernel D_s
alpha = (1/15) * 1e3            # Parameter for Kernel D, eq.(2.29)
K = 2                           # Stimulus Spatial Frequency
omega = 8*np.pi                 # Stimulus temporal frequency
dt = 1e-3                       # Time step
t = np.arange(0, 1, dt)         # Time array
tau = np.arange(0, 0.3, dt)     # Tau array for calculating D
x = np.arange(-2, 2, 0.1)       # X array
y = np.arange(-2, 2, 0.1)       # Y array

# --- Constructing Stimulus ---
# Initializing stimulus array S
S = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(t)[0]))
# Calculating stimulus for each time point n and each x and y
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        for n in range(np.shape(t)[0]):
            S[i, j, n] = np.cos(K*x[i] - omega*t[n])

# --- Constructing Kernel ---
# Initializing spatial kernel D_s(x, y)
D_s = np.zeros((np.shape(x)[0], np.shape(y)[0]))
# Calculating D_s(x, y) for each x and y (equation 2.27)
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        D_s[i, j] = ((1 / (2*np.pi*sigma))
                    * (np.exp((-x[i]**2 - y[j]**2)/(2*sigma**2)))
                    * (np.cos(k*x[i] - phi)))
# Calculating temporal kernel D_t(tau) (equation 2.29)
D_t = (
alpha
* np.exp(-alpha*tau)
* (((alpha*tau)**5)/factorial(5) - ((alpha*tau)**7)/factorial(7))
)
D_t = np.flip(D_t)  # Reversing D_t to calculate integral (2.24) easier 
# Calculatind kernel D(x, y, tau) = D_s * D_t
D = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(tau)[0]))
for i in range(np.shape(tau)[0]):
    D[:, :, i] = D_t[i] * D_s

# --- Calculating the linear estimate of response (as a function of time) ---
# Initializing estimated response array
L = np.zeros(np.shape(t))
# Calculating eastimated response according to eq.(2.24)
for i in range(np.shape(L)[0]):
    if (np.shape(D)[2] - i) > 0:
        d = D[:, :, 0:i]
        s = S[:, :, 0:i]
        L[i] = np.sum(np.sum(s * d))
    else:
        s = S[:, :, i-np.shape(D)[2]:i]
        L[i] = np.sum(np.sum(s * D))
# Rectifying response
L[np.where(L < 0)] = 0
# plot response as a function of time
plt.plot(t, L)
plt.xlabel('Time [second]')
plt.ylabel('Response L(t)')

# ----------------------------------------------------------------------------
# --- Constructing Stimulus (for different values of omega) ---
# ----------------------------------------------------------------------------
omega = np.arange(0, 16*np.pi, np.pi)
# Initializing stimulus array S
S = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(t)[0], np.shape(omega)[0]))
# Calculating stimulus for each time point and each x and y and different omega
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        for n in range(np.shape(t)[0]):
            for o in range(np.shape(omega)[0]):
                S[i, j, n, o] = np.cos(K*x[i] - omega[o]*t[n])

# --- Calculating the linear estimate of response (as a function of time) ---
# Initializing estimated response array
L = np.zeros((np.shape(omega)[0], np.shape(t)[0]))
# Calculating eastimated response according to eq.(2.24)
for j in range(np.shape(omega)[0]):
    for i in range(np.shape(L)[1]):
        if (np.shape(D)[2] - i) > 0:
            d = D[:, :, 0:i]
            s = S[:, :, 0:i, j]
            L[j, i] = np.sum(np.sum(s * d))
        else:
            s = S[:, :, i-np.shape(D)[2]:i, j]
            L[j, i] = np.sum(np.sum(s * D))
# Rectifying response
L[np.where(L < 0)] = 0
# plot response as a function of time for different omegas
plt.figure()
plt.plot(omega, np.amax(L, axis = 1))
plt.xlabel('omega [Hz]')
plt.ylabel('Max Amplitude')

# ----------------------------------------------------------------------------
# --- Constructing Stimulus (for different values of K) ---
# ----------------------------------------------------------------------------
omega = 8*np.pi                 # Stimulus temporal frequency
K = np.arange(0, 4, 0.1)
# Initializing stimulus array S
S = np.zeros((np.shape(x)[0], np.shape(y)[0], np.shape(t)[0], np.shape(K)[0]))
# Calculating stimulus for each time point and each x and y and different omega
for i in range(np.shape(x)[0]):
    for j in range(np.shape(y)[0]):
        for n in range(np.shape(t)[0]):
            for o in range(np.shape(K)[0]):
                S[i, j, n, o] = np.cos(K[o]*x[i] - omega*t[n])

# --- Calculating the linear estimate of response (as a function of time) ---
# Initializing estimated response array
L = np.zeros((np.shape(K)[0], np.shape(t)[0]))
# Calculating eastimated response according to eq.(2.24)
for j in range(np.shape(K)[0]):
    for i in range(np.shape(L)[1]):
        if (np.shape(D)[2] - i) > 0:
            d = D[:, :, 0:i]
            s = S[:, :, 0:i, j]
            L[j, i] = np.sum(np.sum(s * d))
        else:
            s = S[:, :, i-np.shape(D)[2]:i, j]
            L[j, i] = np.sum(np.sum(s * D))
# Rectifying response
L[np.where(L < 0)] = 0
# plot response as a function of time for different K
plt.figure()
plt.plot(K, np.amax(L, axis = 1))
plt.xlabel('K')
plt.ylabel('Max Amplitude')


plt.show()

