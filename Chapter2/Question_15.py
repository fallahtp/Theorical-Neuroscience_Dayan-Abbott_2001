"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 2 : Reverse Correlation and Visual Receptive Fields
Question 15
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# --- Imports ---
import numpy as np
import matplotlib.pyplot as plt

# --- Setting parameters ---
sigma_c = 0.3
sigma_s = 1.5
B = 5
K = np.arange(-10, 10, 0.1)        # Stimulus Spatial Frequency
x = np.arange(-2, 2, 0.1)       # X array
y = np.arange(-2, 2, 0.1)       # Y array

# --- Constructing 3 on-center and 6 off-center kernels eq.(2.45) ---
# Initializing on-center array of 3 on-center cells  
D_on = np.zeros((np.shape(x)[0], np.shape(y)[0], 3))
# Calculating kernel D for each x and y, for each on-center cells
y_c = [0, 0.6, -0.6]
for c in range(3):
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(y)[0]):
            D_on[i, j, c] = (
                ((1/(2*np.pi*(sigma_c**2))) * np.exp(((x[i]-0)**2 + (y[j]+y_c[c])**2)/(-2*(sigma_c**2))))
                - ((B/(2*np.pi*(sigma_s**2))) * np.exp(((x[i]-0)**2 + (y[j]+y_c[c])**2)/(-2*(sigma_s**2))))
            )
# Initializing off-center array of 6 off-center cells  
D_off = np.zeros((np.shape(x)[0], np.shape(y)[0], 6))
# Calculating kernel D for each x and y for each off-center cells
y_c = [0, 0.6, -0.6]
x_c = [-0.6, 0.6]
c = 0 
for c2 in range(2):
    for c1 in range(3):
        for i in range(np.shape(x)[0]):
            for j in range(np.shape(y)[0]):
                D_off[i, j, c] = -(
                    ((1/(2*np.pi*(sigma_c**2))) * np.exp(((x[i]-x_c[c2])**2 + (y[j]+y_c[c1])**2)/(-2*(sigma_c**2))))
                    - ((B/(2*np.pi*(sigma_s**2))) * np.exp(((x[i]-x_c[c2])**2 + (y[j]+y_c[c1])**2)/(-2*(sigma_s**2))))
                )
        c += 1
# Sum of all cells
D_on = np.sum(D_on, axis=2)     # Sum of 3 on-center Cells
D_off = np.sum(D_off, axis=2)   # Sum of 6 off-center Cells
D = D_on + D_off                # Sum of on-center and off-center Cells
# Plot
plt.pcolormesh(x, y, D.T, shading='nearest')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Sum of 9 LGN Neurons')
plt.show()









