"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 3
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat                                        # This function is used to load .mat files.

# --- Loading Data ---
data   = loadmat('c2p3.mat')                                        # Load data from .mat file 'c2p3.mat'
counts = data['counts'][:, 0]                                       # Get counts from data dict with key = 'counts'
stim   = data['stim'].astype('double')                              # Get stim from data dict with key = 'stim', and converted its type to double

# --- Calculating STA ---
spike_index = np.where(counts != 0)[0]                              # Finding indexes where we have any spike 
STA         = np.zeros((16, 16, 12))                                # Initializing STA Array, 16 x 16 images for 12 time step
for i in range(1, 13):                                              # Loop through each 12 time step and calculate corresponding STA
    c   = 0                                                         # Initializing counter to use in averaging
    sta = np.zeros((16, 16))                                        # Initializing sta array for calculating sta for each time step
    for index in spike_index:                                       # Loop through each spike index and calculate sta for ith time step before spike
        try:                             
            sta = sta + (counts[index] * stim[:, :, index - i])     # Finding Stimulus at given time step before each spike and add it to sta with the weight of number of spikes
            c   =  c + counts[index]                                # Add number of spikes into c to calculate average at the end of this loop
        except:                                                     # In the case that stimulus is not defined for ith time step and for spesific spike
            continue
    sta           = sta / c                                         # Averaging sta by dividing sta with total number of spikes
    STA[:, :, -i] = sta                                             # Inserting sta to corresponding place in STA array, According to time step i

# --- Plots ---
tau = []                                                            # Calculalting tau for each time step to use in plots
for i in range(1, 13):
    tau.append(i * 15.6)
tau.reverse()

sta_fig = plt.figure()
sta_fig.suptitle('Spike-Triggered Average', fontsize = 16)
for i in range(12):
    plt.subplot(3, 4, i+1)
    plt.imshow(STA[:, :, i], 'gray')
    plt.xticks([])
    plt.yticks([])
    plt.title('\u03C4' + ' = ' + str(-tau[i]))
    if i == 8:
        plt.xlabel('X')
        plt.ylabel('Y')

plt.figure()
x_tau = np.sum(STA, axis = 0)
plt.imshow(x_tau, 'gray')
plt.xticks(ticks=[0, 5, 11], labels = [-tau[0], -tau[5], -tau[11]])
plt.xlabel('\u03C4 [ms]')
plt.ylabel('Y')
plt.title('Space-Time Receptive field')

plt.show()







