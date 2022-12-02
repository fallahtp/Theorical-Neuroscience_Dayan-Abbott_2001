"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 1 : Firing Rates and Spike Statistics
Question 4
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
t_end   = 1                   # Final Time  [Second]
dt      = 1e-5                # Time Step   [Second]

# --- Spike Train Generation ---
tau_approx_list = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]                    # Create a list for approximation time constants
r_approx_array  = np.zeros((len(tau_approx_list), int(t_end/dt)))                    # Initializing approximated firing rate array (for store r_approximate in each time step)
c               = 0                                                                  # Counter for changing rows of r_approx_array for each tau_approx
for tau_approx in tau_approx_list:                                                   # Loop through each Approximation Time Constant in tau_approx_list
    r              = []                                                              # Initializing real firing rate list (for store r_approximate in each time step)
    r_approx       = 0                                                               # Set r_approximate to 0
    spike_train    = np.zeros((1, int(t_end/dt)))                                    # Initialize Spike Train Array
    for t in range(0, int(t_end/dt)):                                                # Loop for every Time Step
        r_t                   = 100 * (1 + np.cos(2 * np.pi * (t*dt)/0.3))           # Calculating firing rate for each time step
        r.append(r_t)                                                                # Store firing rate in r
        r_approx              = r_approx + ((-r_approx/(tau_approx * 1e-3)) * dt)    # Approximating firing rate for each time step
        r_approx_array[c, t]  = (r_approx)                                           # Store approximated firing rate in r_approx_array
        x_rand                = random.uniform(0, 1)                                 # Choose a random number uniformly from [0, 1]
        if (r_t * dt) > x_rand:                                                      # Check Spike condition and change correspond element to 1 if there is a spike
            spike_train[0, t] = 1
            r_approx += 1/(tau_approx * 1e-3)                                        # Updating Approximated firing rate after each spike
    c += 1                                                                           # Update Counter

# --- Calculating Average Squered Error ---
average_squered_error = np.mean((r_approx_array - r) ** 2, axis = 1)                 # Average Squered Error

# --- Plots ---
time      = np.arange(0, t_end-dt, dt)    # Creating Time array for plots
tau_index = 5                             # Choose tau_approximate from 'tau_approx_list', with its index, to plot
plt.figure()
plt.plot(time, r)
plt.plot(time, r_approx_array[tau_index, :])
plt.legend(["Real", "Estimated (tau = " + str(tau_approx_list[tau_index]) + " ms)"])
plt.xlabel("Time [Second]")
plt.ylabel("Firing Rate [Hz]")
plt.title("Real and Estimated Firing Rates")

plt.figure()
plt.plot(tau_approx_list, average_squered_error)
plt.xlabel("Approximation Time Constant (tau) [ms]")
plt.ylabel("Average Squered Error [Hz^2]")
plt.title("Average Squered Error")
plt.show()









