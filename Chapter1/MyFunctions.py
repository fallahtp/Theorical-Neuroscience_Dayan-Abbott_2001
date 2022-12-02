"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
This module included functions that are used in questions of chapter 1 and for the sake of abbriviation and simplicity, we collect them here and then we import this module when it's needed. 
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

# --- Computing Spike Times ---
def spike_times(spike_train, dt):
    """
    This Function take the spike_train array and dt, and return spike times
    """
    spike_times = []                              # Initialize Spike Times Array
    for i in range(spike_train.shape[1]):         # Loop through all elements of spike_train
        if spike_train[0, i] == 1:                # Check if there is a spike
            time = i * dt                         # Change element index to Time in second
            spike_times.append(time)              # Append spike time to spike_times Array
    return spike_times

# --- Computing InterSpike Intervals (ISI) ---
def ISI(spike_times):
    """
    This Function get spike time and return InterSpikeInterval
    """
    ISI = []                                      # Initialize ISI Array
    for i in range(len(spike_times) - 1):         # Loop through all spike times
        t1  = spike_times[i]                      # t_i
        t2  = spike_times[i + 1]                  # t_i+1
        isi = t2 - t1                             # isi = t_i+1 - t_i
        ISI.append(isi)                           # Append isi to ISI Array
    return ISI

# --- Computing Coefficient of Variation (Cv) ---
def Cv(ISI):
    """
    This Function get InterSpikeIntervals and return Coefficient of Variation (Cv)
    """
    std_isi  = np.std(ISI)                        # Calculating Standard deviation of ISI s.
    mean_isi = np.mean(ISI)                       # Calculating mean of ISI s.
    Cv       = std_isi / mean_isi                 # Calculating Cv
    print("\n", "The Coefficient of Variation of the InterSpikeIntervals is :", Cv, "\n")
    return Cv

# --- Computing Fanon Factor ---
def FF(spike_train, counting_interval, dt):
    """
    This Function take spike_train, counting_interval [ms], dt and return Fanon Factor 
    """
    c_i               = int(counting_interval/(1000*dt))      # Number of elements in a window
    num_intervals     = floor(spike_train.shape[1]/c_i)       # Number of intervals
    intervals         = np.zeros((num_intervals, c_i))        # Initialize intervals Array for seperating intervals
    for i in range(num_intervals - 1):                        # Loop for seperating intervals
        start           = i * c_i                             # Strat index for ith interval
        stop            = (i + 1) * c_i                       # Stop index for ith interval
        intervals[i, :] = spike_train[0, start:stop]          # Seperating ith interval from spike train
    spike_count = np.sum(intervals, axis = 1)                 # Counting spikes in each interval
    ff = np.var(spike_count) / np.mean(spike_count)           # Calculating Fanon Factor FF = var(spike_count) / mean(spike_count)
    return ff

# --- Calculating AutoCorrelation ---
def Auto_corr(spike_times):
    """
    This Function Calculate Spike Train AutoCorrelation by calculating ISI between any two spikes in the spike train
    """
    Autocorrelation = []                                      # Initialized autocorrelation array
    for i in spike_times:                                     # Take one spike time in this loop
        for j in spike_times:                                 # Take an other spike time in this loop
            autocorrelation = i - j                           # Calculating InterSpikeInterval between two spike times 
            Autocorrelation.append(autocorrelation)           # Append calculated ISI to the autocorrelation array
    return Autocorrelation



