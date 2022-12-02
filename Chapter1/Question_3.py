"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 3
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
t_end   = 20         # Final Time  [Second]
dt      = 1e-5       # Time Step   [Second]
r       = 100        # Firing Rate [Hz]
r0      = 100        # Firing Rate [Hz]
tau_ref = 10         # Refractory period [ms]

# --- Computing Spike Train ---
# First part [r = 100]
spike_train1 = np.zeros((1, int(t_end/dt)))   # Initialize Spike Train Array
for t in range(0, int(t_end/dt)):            # Loop for every Time Step
    x_rand = random.uniform(0, 1)            # Choose a random number uniformly from [0, 1]
    if (r * dt) > x_rand:                    # Check Spike condition and change correspond element to 1 if there is a spike
        spike_train1[0, t] = 1

# Second part [r = 100, refractory = 10 ms]
spike_train2 = np.zeros((1, int(t_end/dt)))          # Initialize Spike Train Array
for t in range(0, int(t_end/dt)):                    # Loop for every Time Step
    x_rand = random.uniform(0, 1)                    # Choose a random number uniformly from [0, 1]
    r = r +  (((r0-r) * dt) / (tau_ref * 1e-3))      # Refractory, r converge exponentialy to r0
    if (r * dt) > x_rand:                            # Check Spike condition and change correspond element to 1 if there is a spike
        spike_train2[0, t] = 1
        r = 0                                        # Set firing rate to zero afrer spike
    
# Third part [r(t) = 100 * (1 + np.cos(2 * np.pi * t / 25))]
spike_train3 = np.zeros((1, int(t_end/dt)))   # Initialize Spike Train Array
for t in range(0, int(t_end/dt)):            # Loop for every Time Step
    r_t = 100 * (1 + np.cos(2 * np.pi * (t*dt)/0.025))
    x_rand = random.uniform(0, 1)            # Choose a random number uniformly from [0, 1]
    if (r_t * dt) > x_rand:                    # Check Spike condition and change correspond element to 1 if there is a spike
        spike_train3[0, t] = 1

# --- Computing Spike Times ---
spike_times1 = mf.spike_times(spike_train1, dt)   # Use Function spike_times in MyFunctions module
spike_times2 = mf.spike_times(spike_train2, dt)   # Use Function spike_times in MyFunctions module
spike_times3 = mf.spike_times(spike_train3, dt)   # Use Function spike_times in MyFunctions module

# --- Computing AutoCorrelation ---
Autocorrelation1 = mf.Auto_corr(spike_times1)     # Use Function 'Auto_corr' in MyFunctions module 
Autocorrelation2 = mf.Auto_corr(spike_times2)     # Use Function 'Auto_corr' in MyFunctions module
Autocorrelation3 = mf.Auto_corr(spike_times3)     # Use Function 'Auto_corr' in MyFunctions module

# --- This Function Plot AutoCorrelation histogram
def plot_hist(Autocorrelation):
    plt.figure()
    bins           = []                                 # Initialize bins for histogram
    final_bin_edge = 100                                # Final bin edge [in ms]
    bin_size       = 1                                  # Bin size [ms]
    for i in range(0, final_bin_edge, bin_size):        # Calculating bins from 0 to final_bin_edge ms, bin size = bin_size ms
        bins.append(i/1000)
    plt.hist(Autocorrelation, bins = bins)              # Plot histogam
    plt.xticks(ticks = [0, 0.02, 0.04, 0.06, 0.08, 0.1], labels = [0, 20, 40, 60, 80, 100])
    plt.xlabel('InterSpikeInterval [ms]')
    plt.ylabel("Count of isi")
    plt.title('Histogram of ISI')
    plt.show()

# --- Plot Histograms ---
autoCorrelation_list = [Autocorrelation1, Autocorrelation2, Autocorrelation3]   # Make a list of autocorrelation 
for auto in autoCorrelation_list:                                               # Plot one AutoCorrelation in each iteration
    plot_hist(auto)

