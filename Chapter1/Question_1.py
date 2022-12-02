"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 1
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
t_end = 20         # Final Time  [Second]
dt    = 1e-5       # Time Step   [Second]
r     = 100        # Firing Rate [Hz]

# --- Computing Spike Train ---
spike_train = np.zeros((1, int(t_end/dt)))   # Initialize Spike Train Array
for t in range(0, int(t_end/dt)):            # Loop for every Time Step
    x_rand = random.uniform(0, 1)            # Choose a random number uniformly from [0, 1]
    if (r * dt) > x_rand:                    # Check Spike condition and change correspond element to 1 if there is a spike
        spike_train[0, t] = 1

# --- Computing Spike Times ---
spike_times = mf.spike_times(spike_train, dt)   # Use Function spike_times in MyFunctions module

# --- Computing InterSpike Intervals (ISI) ---
ISI = mf.ISI(spike_times)                       # Use Function ISI in MyFunctions module

# --- Computing Coefficient of Variation (Cv) ---
Cv = mf.Cv(ISI)                                 # Use Function Cv in MyFunctions module

# --- Computing Fanon Factor (FF) for spike counts obtained over counting interval ---
FF          = []                                              # Initialize fanon factor Array
window_size = []                                              # Initialize counting window duration
for j in range(5, 101, 5):                                    # Loop through different window size ranging from 5 - 100 ms
    counting_interval = j                                     # Counting interval in ms
    window_size.append(j)                                     # Append counting window into window_size (for plot)
    ff = mf.FF(spike_train, counting_interval, dt)            # Use Function FF in Myfunctions module
    FF.append(ff)                                             # Appending to FF (in order to plot)
plt.figure()                                                  # Plot FF vs. count duration
plt.title("Fanon Factor for different counting duration")
plt.plot(window_size, FF, 'ok')
plt.xlabel("Count duration [ms]")
plt.ylabel('Fanon Factor')

# --- ISI histogram ---
plt.figure()
bins           = []                                 # Initialize bins for histogram
final_bin_edge = 80                                 # Final bin edge [in ms]
bin_size       = 5                                  # Bin size [ms]
for i in range(0, final_bin_edge, bin_size):        # Calculating bins from 0 to 80 ms, bin size = 5 ms
    bins.append(i/1000)
plt.hist(ISI, bins = bins)                          # Plot histogam
plt.xticks(ticks = [0, 0.02, 0.04, 0.06, 0.08], labels = [0, 20, 40, 60, 80])
plt.xlabel('InterSpikeInterval [ms]')
plt.ylabel("Count of isi")
plt.title('Histogram of ISI')
plt.show()



