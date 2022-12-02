"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 2
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.io import loadmat             # This function is used to load .mat files.
from scipy.ndimage.interpolation import shift                                               # This function is used to calculate correlations

# --- Loading Data ---
data = loadmat("c1p8.mat")               # Loading data from "c1p8.mat" file (data is a dictionary)
rho  = data["rho"]                       # Take spike train from data with (key = rho)
stim = data["stim"]                      # Take stimulus values from data with (key = stim)
dt   = 2e-3                              # Time step [Second]
r0   = 45

# --- Calculating spike Indexes ---
spike_index = []                         # Initializing spike index list to store spike indexes in each loop
for i in range(np.shape(rho)[0]):        # Loop through every element in spike train (rho) to find spike indexes
    if rho[i, 0] == 1:                   # Check whether there is a spike or not
        spike_index.append(i)            # If there is a spike append its index to spike_index

# --- Calculating STA ---
sta = np.zeros((len(spike_index), 150))  # Initializing sta array with (number of spikes) rows and (300) columns (from -300 ms to 300 ms)
c   = 0                                  # Initializing counter for changing rows of sta in following loop
for index in spike_index:                # Loop through each spike and crop a window from -150 to 150 point from stimulus in each spike time
    start = index - 150                  # Calculating starting index of the window for given spike index
    stop  = index                        # Calculating final index of the window for given spike index
    if start < 0:                        # Checking whether starting index is less than 0
        continue                         # Ignor this spike (going to the next iteration)
    if stop > np.shape(stim)[0]:         # Checking whether stop index is more than end index of the stimulus
        continue                         # Ignor this spike (going to the next iteration)
    sta[c, :] = stim[start:stop, 0]      # Crop Stimulus with the window and insert the croped part in the sta 
    c += 1                               # Updating counter to go to the next row of sta in next iteration
STA = np.mean(sta, axis=0)               # STA is average of all croped part of the stimulus stored in sta

# --- Use STA To construct Kernel D ---
stimulus = stim[:, 0]
r_avg = np.sum(rho, axis = 0) / (20*60)
sigma_s2 = np.var(stimulus)
D = r_avg[0] * STA / sigma_s2

# --- Estimating Firing Rate ---

r_est = r0 * np.ones((len(stimulus)))                                                      # Initializing estimated Firing rate Array
D     = np.flip(D)                                                                          # Reverting D(tau) to estimating firing rate in following for loop
for i in range(len(stimulus)):                                                                  # Loop through each time point and calculate corresponding firing rate
    if i < 150:                                                                              # Because for i < 30 we don't have stimulus for each point in D, to calculate S(t - tau), so we shorten our calculation of eq.(2.1) to points we have from the stimulus
        s        = stimulus[0:i]                                                            # Cut corresponding part of the stimulus
        d        = D[0:i]                                                                   # Cut corresponding part of the Kernel D
        r_est[i] = r0 + np.sum(s * d)                                                       # Equation 2.1
    elif i >= 150:
        s        = stimulus[i-150: i]                                                        # Cut corresponding part of the stimulus
        r_est[i] = r0 + np.sum(s * D)                                                       # Equation 2.1

spike_train = np.zeros((np.shape(r_est)))
for i in range(len(r_est)):
    x_rand = random.uniform(0, 1)
    if r_est[i] * dt > x_rand:
        spike_train[i] = 1

# Calculating AutoCorrelations ---
Q_act = np.zeros((50,))
for i in range(len(Q_act)):
    rho_shift = shift(rho[:, 0], i)
    Q_act[i] = np.mean(rho[:, 0] * rho_shift)

Q_syn = np.zeros((50,))
for i in range(len(Q_syn)):
    spike_train_shift = shift(spike_train, i)
    Q_syn[i] = np.mean(spike_train * spike_train_shift)


plt.plot(Q_act)
plt.figure()
plt.plot(Q_syn)
plt.figure()
plt.plot(r_est)
plt.figure()
plt.plot(rho[1000:2000, 0])
plt.figure()
plt.plot(spike_train[1000:2000], 'red')
plt.show()

















