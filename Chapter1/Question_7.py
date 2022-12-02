"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 7
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
t_end   = 10                                # Final Time  [Second]
dt      = 1e-4                              # Time Step   [Second]
time    = list(np.arange(dt, t_end, dt))    # Time array
r0      = 10                                # Background Firing rate [Hz]
tau_r   = 20                                # Time Constant [ms]

# --- Bilding Stimulus ---
stimulus           = np.zeros((1, floor(t_end/dt)))               # Initialize Stimulus Array
for i in range(len(time)):                                        # Loop through each time point
    sigma_s        = 0.01                                         # Stimulus varibility
    var            = (sigma_s ** 2)/dt                            # Stimulis Variance
    x_rand         = random.gauss(mu = 0, sigma = np.sqrt(var))   # Generaate a rendom number from a gaussian distribution
    stimulus[0, i] = x_rand                                       # Place the random number in the stimulus array

# --- Simulation Firing rate model ---
r_est           = r0 * np.ones((1, floor(t_end/dt)))              # Initialize estimated response Array
for i in range(len(time) - 1):  
    r_est[0, i + 1] = r_est[0, i] + ((np.abs(r0 + stimulus[0, i]) - r_est[0, i]) * (dt/(tau_r*1e-3)))

# --- Calculating Stimulus-Response Correlation function ---
Q_rs = np.correlate(stimulus[0, :], r_est[0, :], mode = "full")

# --- Computing Spike Train ---
spike_train = np.zeros((1, int(t_end/dt)))   # Initialize Spike Train Array
for t in range(0, int(t_end/dt)):            # Loop for every Time Step
    x_rand = random.uniform(0, 1)            # Choose a random number uniformly from [0, 1]
    if (r_est[0, t] * dt) > x_rand:          # Check Spike condition and change correspond element to 1 if there is a spike
        spike_train[0, t] = 1

# --- Computing Spike Times ---
spike_index = np.where(spike_train[0, :] == 1)[0]

# --- Calculating STA ---
win = int(30 * 1e-3 /dt)                 # Window Size
# --- Calculating STA ---
sta = np.zeros((len(spike_index), win))  # Initializing sta array with (number of spikes) rows and (300) columns (from -300 ms to 300 ms)
c   = 0                                  # Initializing counter for changing rows of sta in following loop
for index in spike_index:                # Loop through each spike and crop a window from -150 to 150 point from stimulus in each spike time
    start = index - win                  # Calculating starting index of the window for given spike index
    stop  = index                        # Calculating final index of the window for given spike index
    if start < 0:                        # Checking whether starting index is less than 0
        continue                         # Ignor this spike (going to the next iteration)
    if stop > np.shape(stimulus)[1]:     # Checking whether stop index is more than end index of the stimulus
        continue                         # Ignor this spike (going to the next iteration)
    sta[c, :] = stimulus[0, start:stop]  # Crop Stimulus with the window and insert the croped part in the sta 
    c += 1                               # Updating counter to go to the next row of sta in next iteration
STA = np.mean(sta, axis=0)               # STA is average of all croped part of the stimulus stored in sta

# --- Plots ---
plt.plot(STA)
plt.figure()
plt.plot(Q_rs)
plt.show()








