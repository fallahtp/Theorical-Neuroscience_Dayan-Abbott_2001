"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 1
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage.interpolation import shift                                               # This function is used to calculate correlations

# --- Set Parameters ---
dt       = 10 * 1e-3                                                                        # Time step [Second]
t_end    = 10                                                                               # End time [Second]
time     = np.arange(0, t_end, dt)                                                          # Time Array
sigma_s2 = 10                                                                               # Stimulus Variance (without dt division)
r0       = 50                                                                               # Background Firing Rate [Hz]

# --- Constructing Stimulus ---
stimulus = np.zeros((np.shape(time)))                                                       # Initializing Stimulus Array
for i in range(len(time)):                                                                  # Loop Through each time point to construct stimulus
    stimulus[i] = random.gauss(mu = 0, sigma = np.sqrt(sigma_s2/dt))                        # Choose a random number in each iteration and set it to stimulus at corresponding index

# --- Computing D(tau) ---
tau = np.arange(0, 0.3, dt)                                                                 # Tau Array for Calculating D(tau)
D   = np.zeros((np.shape(tau)))                                                             # Initilizing D(tau) array
for i in range(len(tau)):                                                                   # Loop through each tau and calculate corresponding D(tau)
    D[i] = (-np.cos(2 * np.pi * (tau[i]*1e3 - 20) / 140)) * np.exp(-tau[i]*1e3 / 60)        # Calculating D(tau) for corresponding tau according to equation in the question

# --- Estimating Firing Rate ---
r_est = r0 * np.ones((np.shape(time)))                                                      # Initializing estimated Firing rate Array
D     = np.flip(D)                                                                          # Reverting D(tau) to estimating firing rate in following for loop
for i in range(len(time)):                                                                  # Loop through each time point and calculate corresponding firing rate
    if i < 30:                                                                              # Because for i < 30 we don't have stimulus for each point in D, to calculate S(t - tau), so we shorten our calculation of eq.(2.1) to points we have from the stimulus
        s        = stimulus[0:i]                                                            # Cut corresponding part of the stimulus
        d        = D[0:i]                                                                   # Cut corresponding part of the Kernel D
        r_est[i] = r0 + np.sum(s * d)                                                       # Equation 2.1
    elif i >= 30:
        s        = stimulus[i-30: i]                                                        # Cut corresponding part of the stimulus
        r_est[i] = r0 + np.sum(s * D)                                                       # Equation 2.1

# --- Calculating FiringRate-Stimulus Revese Correlation Q_rs ---
Q_rs = np.zeros(np.shape(tau))                                                              # Initializing Reverse Correlation Array
for i in range(np.shape(tau)[0]):                                                           # Loop through each tau and calculate reverse correlation
    s = shift(stimulus, i+1)                                                                # Shift stimulus to calculate reverse correlation
    Q_rs[i] = np.mean(r_est * s)                                                            # Calculating Reverse Correlation corresponding to each tau
Q_rs = (Q_rs) / np.var(stimulus)                                                            # Dividing Reverse Correlation by Stimulus variance to Calculate Kernel D, According to eq.(2.6)

# --- Plot ---
plt.figure()                                                                                # Plot Both Kernels and compaire
plt.plot(np.flip(D))
plt.plot(Q_rs, 'red')
plt.xticks([0, 5, 10, 15, 20, 25, 30], labels = [0, 50, 100, 150, 200, 250, 300])
plt.xlabel('Tau [ms]')
plt.ylabel('D (tau)')
plt.legend(['From Equation', 'From Revese Correlation'])
plt.title('Kernels')
plt.show()






