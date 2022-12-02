"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 9
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
from scipy.io import loadmat                                     # This function is used to load .mat files.
from scipy.ndimage.interpolation import shift                    # This Function is used to shift the sta for sum of two single spike triggered average
import MyFunctions as mf                                         # This is The module that include all the functions that we need here, and for simplicity we collect them in MyFunctions.py

# --- Loading Data ---
data = loadmat("c1p8.mat")                                       # Loading data from "c1p8.mat" file (data is a dictionary)
rho  = data["rho"]                                               # Take spike train from data with (key = rho)
stim = data["stim"]                                              # Take stimulus values from data with (key = stim)
dt   = 2e-3                                                      # Time step [Second]

# --- Two-Spike Triggered average Calculation ---
sep_intervals = [2, 4, 10, 50, 100]                              # Seperated interval between two spikes [ms]
TSTA          = np.zeros((len(sep_intervals), 150))              # Initializing Two-Spike Triggered Average array (each row  corresponded to one interval in 'sep_intervals' list) (150 is the number of time points for 300 ms (dt = 2 ms))
c2            = 0                                                # Initializing Counter for changing rows of TSTA 
for sep_interval in sep_intervals:                               # Loop through each seperation interval in 'sep_intervals' and calculate TSTA for each of them
    pattern = [1] + (int(sep_interval/(dt*1e3)) - 1)*[0] + [1]   # Make The pattern of Spike that we needed ([1, 0, ..., 0, 1] number of zeros choose according to seperation interval)
    conv = np.convolve(pattern, rho[:, 0])                       # Concolving the pattern with spike train to find pattern in the spike train
    index = list(np.where(conv == 2)[0])                         # Find index of the spike train where it contain our pattern

    tsta = np.zeros((len(index), 150))                         # Initializing tsta array with (number of Two-spikes) rows and (150) columns (from -300 ms to 0 ms)
    c    = 0                                                   # Initializing Counter for changing rows of tsta
    for i in index:                                            # Loop through each two spike and calculate tsta
        start = i -150                                         # Starting point for tsta window
        stop  = i                                              # Stop point for tsta window
        if start < 0:                                          # Checking whether starting index is less than 0
            continue                                           # Ignor this spike (going to the next iteration)
        if stop > np.shape(stim)[0]:                           # Checking whether stop index is more than end index of the stimulus
            continue                                           # Ignor this spike (going to the next iteration)
        tsta[c, :] = stim[start:stop, 0]                       # Crop Stimulus with the window and insert the croped part in the sta 
        c += 1                                                 # Updating counter to go to the next row of sta in next iteration
    TSTA[c2, :] = np.mean(tsta, axis=0)                        # Insert Calculated tsta of given seperated interval to the TSTA
    c2 += 1                                                    # Update Counter to go to the next row of TSTA for next seperation interval

# --- Calculating STA ---
spike_index = np.where(rho == 1)[0]                            # Finding spike Indexes
sta         = np.zeros((len(spike_index), 150))                # Initializing sta array with (number of spikes) rows and (300) columns (from -300 ms to 300 ms)
c           = 0                                                # Initializing counter for changing rows of sta in following loop
for index in spike_index:                                      # Loop through each spike and crop a window from -150 to 150 point from stimulus in each spike time
    start = index - 150                                        # Calculating starting index of the window for given spike index
    stop  = index                                              # Calculating final index of the window for given spike index
    if start < 0:                                              # Checking whether starting index is less than 0
        continue                                               # Ignor this spike (going to the next iteration)
    if stop > np.shape(stim)[0]:                               # Checking whether stop index is more than end index of the stimulus
        continue                                               # Ignor this spike (going to the next iteration)
    sta[c, :] = stim[start:stop, 0]                            # Crop Stimulus with the window and insert the croped part in the sta 
    c += 1                                                     # Updating counter to go to the next row of sta in next iteration
STA = np.mean(sta, axis=0)                                     # STA is average of all croped part of the stimulus stored in sta

# --- Sum of Two STA  ---
sum_STA = np.zeros(np.shape(TSTA))                             # Initializing sum_STA array for calculating sum of two shifted STA which seperated by same separation interval of TSTA
c       = 0                                                    # Initializing Counter to 0 for changing rows of 'sum_STA'
for sep_interval in sep_intervals:                             # Loop through each seperation interval to calculate  sum_STA for it
    shifted_STA   = shift(STA, -int(sep_interval/(dt*1e3)))    # Shift STA backward for 'seperation interval' number of time points
    sum_STA[c, :] = shifted_STA + STA                          # Calculating sum_STA for given seperation interval
    c += 1                                                     # Updating Counter to go to the next row of sum_STA for next seperation interval

# --- Mean Squared Difference ---
diff_sta = np.mean(np.abs(TSTA - sum_STA)**2, axis = 1)        # Calculating Mean Squared Difference between TSTA and sum_STA

# --- Plot ---
for i in range(len(sep_intervals)):                            # Plot TSTA for Different seperation intervals
    plt.plot(np.arange(-0.3, 0, dt) * 1000, TSTA[i, :])
plt.xlabel("Time [ms]")
plt.ylabel("TSTA")
plt.title("Two-Spike Triggered Average")
plt.legend(['2 ms', '4 ms', '10 ms', '50 ms', '100 ms'])

plt.figure()                                                   # Plot Mean Squared Difference between TSTA and sum_STA for different seperation intervals
plt.plot(sep_intervals, diff_sta, 'ok')
plt.xlabel("Seperation Interval [ms]")
plt.ylabel("Mean Squared Difference between TSTA and sum_STA")
plt.title("Mean Squared Difference between TSTA and sum_STA for different seperation intervals")

plt.show()
