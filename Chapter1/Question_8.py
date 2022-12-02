"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 8
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
from scipy.io import loadmat             # This function is used to load .mat files.
import MyFunctions as mf                 # This is The module that include all the functions that we need here, and for simplicity we collect them in MyFunctions.py

# --- Loading Data ---
data = loadmat("c1p8.mat")               # Loading data from "c1p8.mat" file (data is a dictionary)
rho  = data["rho"]                       # Take spike train from data with (key = rho)
stim = data["stim"]                      # Take stimulus values from data with (key = stim)
dt   = 2e-3                              # Time step [Second]

# --- Calculating spike Indexes ---
spike_index = []                         # Initializing spike index list to store spike indexes in each loop
for i in range(np.shape(rho)[0]):        # Loop through every element in spike train (rho) to find spike indexes
    if rho[i, 0] == 1:                   # Check whether there is a spike or not
        spike_index.append(i)            # If there is a spike append its index to spike_index

# --- Calculating STA ---
sta = np.zeros((len(spike_index), 300))  # Initializing sta array with (number of spikes) rows and (300) columns (from -300 ms to 300 ms)
c   = 0                                  # Initializing counter for changing rows of sta in following loop
for index in spike_index:                # Loop through each spike and crop a window from -150 to 150 point from stimulus in each spike time
    start = index - 150                  # Calculating starting index of the window for given spike index
    stop  = index + 150                  # Calculating final index of the window for given spike index
    if start < 0:                        # Checking whether starting index is less than 0
        continue                         # Ignor this spike (going to the next iteration)
    if stop > np.shape(stim)[0]:         # Checking whether stop index is more than end index of the stimulus
        continue                         # Ignor this spike (going to the next iteration)
    sta[c, :] = stim[start:stop, 0]      # Crop Stimulus with the window and insert the croped part in the sta 
    c += 1                               # Updating counter to go to the next row of sta in next iteration
STA = np.mean(sta, axis=0)               # STA is average of all croped part of the stimulus stored in sta


# --- Plot ---
plt.plot(np.arange(-0.3, 0.3, dt), STA)
plt.xlabel("Time [ms]")
plt.ylabel("STA")
plt.title("Spike Triggered Average")
plt.show()








