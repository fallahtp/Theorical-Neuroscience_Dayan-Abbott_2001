"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 6
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
from math import floor
import random
import numpy as np
import matplotlib.pyplot as plt
import MyFunctions as mf   # This is The module that include all the functions that we need here, and for simplicity we collect them in MyFunctions.py

# --- Set Parameters ---
t_end   = 1                           # Final Time  [Second]
dt      = 1e-5                        # Time Step   [Second]
time    = np.arange(dt, t_end, dt)    # Time array

# --- Bilding Stimulus ---
stimulus           = np.zeros((1, floor(t_end/dt)))               # Initialize Stimulus Array
for i in range(len(time)):                                        # Loop through each time point
    sigma_s        = 1                                            # Stimulus varibility
    var            = (sigma_s ** 2)/dt                            # Stimulis Variance
    x_rand         = random.gauss(mu = 0, sigma = np.sqrt(var))   # Generaate a rendom number from a gaussian distribution
    stimulus[0, i] = x_rand                                       # Place the random number in the stimulus array

# --- Calculating Autocorrelation of the Stimulus
corr = np.correlate(stimulus[0, :], stimulus[0, :], mode = "full")

# --- Plots ---
plt.figure()                                                       # Stimulus
plt.plot(time, stimulus[0, :])
plt.ylabel("Amplitude")
plt.xlabel("Time [S]")
plt.title("White Noise Stimulus")

plt.figure()                                                        # Stimulus Power Spectrum
plt.psd(stimulus[0, :], Fs = 1/dt)

plt.figure()                                                        # Stimulus Autocorrelation
plt.plot(np.arange(-t_end+dt+dt, t_end-dt, dt), corr)
plt.ylabel("Correlation")
plt.xlabel("Time [S]")

plt.show()
