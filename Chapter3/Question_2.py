"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 3 : Neural Decoding
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

# --- Set parameters ---
trials = 1000               # Number of trials
dot = ['p', 'n']            # Random dot directions
d = np.arange(0, 10, 1)     # Discriminability

# --- Simulation ---
# Initialuizing Stimulus array with shape = (number of trials) X (number of d)
stim = np.empty((trials, np.shape(d)[0]), dtype=object)
# Initializing rate array with the same shape of stim
r = np.zeros((trials, np.shape(d)[0]))
# In this loop stimulus and rate are calculating for each d and each trial as mentioned in the question
for j in range(np.shape(d)[0]): # Loop through each d
    for i in range(trials):     # Loop through each trial
        stim[i, j] = random.choice(dot)
        if stim[i, j] == 'n':
            r[i, j] = 20 + random.gauss(mu = 0, sigma = 10)
            if (r[i, j] < 0): r[i, j] = 0
        if stim[i, j] == 'p':
            r[i, j] = 20 + (10*d[j]) + random.gauss(mu = 0, sigma = 10)
            if (r[i, j] < 0): r[i, j] = 0

# --- Guess the stimulus ---
# Initializing guess array
guess = np.empty((trials, np.shape(d)[0]), dtype=object)
# Guess each 'p' or 'n' for each trial and each d for threshold z = 20+5d
for j in range(np.shape(d)[0]):
    z = 20 + (5*d[j])
    for i in range(trials):
        if r[i, j] >= z: guess[i, j] = 'p'
        if r[i, j] < z: guess[i, j] = 'n'
# Checking which of our guesses are true
check = (guess == stim)
# Calculating percent of out true guesses for each d
correct_percent = (np.sum(check, axis=0) / trials) * 100
# plot correct percent for each d
plt.plot(d, correct_percent)
plt.ylabel('Correct Guess %')
plt.xlabel('Discriminative (d)')

# ============================================================================
# ROC Curves
# ============================================================================
# setting threshold z in range from 0 to 140
z = np.arange(0, 140, 1)
# Initializing guess array (this time we also store guess for each z (Third dim)) (-2 is for that we want d>2)
guess = np.empty((trials, np.shape(d)[0]-2, np.shape(z)[0]), dtype=object)
# Guess each r is 'p' or 'n' according to each threshold z
for k in range(np.shape(z)[0]):
    for j in range(2, np.shape(d)[0]):
        for i in range(trials):
            if r[i, j] >= z[k]: guess[i, j-2, k] = 'p'
            if r[i, j] < z[k]: guess[i, j-2, k] = 'n'

# Calculating alpha and beta
alpha = np.zeros((np.shape(z)[0], np.shape(d)[0]))  # Initialize alpha array
beta = np.zeros((np.shape(z)[0], np.shape(d)[0]))   # Initialize beta array
# For each z and d, alpha and beta is calculated
for k in range(np.shape(z)[0]):
    for i in range(np.shape(d)[0]-2):
        g = guess[:, i, k]
        s = stim[:, i+2]
        B = 0   # Counter for beta 
        A = 0   # Counter for alpha
        for j in range(np.shape(g)[0]):
            if (g[j] == 'p') and (s[j] == 'p'):
                B += 1
            if (g[j] == 'p') and (s[j] == 'n'):
                A += 1
        alpha[k, i] = A/np.sum(s == 'n')   # Alpha P[plus|-], which is number of plus guesses divided by number of trilas that stimulus is in fact mines
        beta[k, i] = B/np.sum(s == 'p')    # Beta P[plus|+], which is number of plus guesses divided by number of trilas that stimulus is in fact plus

# ROC plots
plt.figure()
for i in range(7):
    plt.plot(alpha[:, i], beta[:, i])
plt.legend(['d=2', 'd=3', 'd=4', 'd=5', 'd=6', 'd=7', 'd=8', 'd=9', 'd=10'])
plt.xlabel('\u03B1')
plt.ylabel('\u03B2')
plt.title('ROC')

plt.show()



