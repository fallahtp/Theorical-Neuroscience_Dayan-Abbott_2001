"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 5 : Model Neurons I: Neuroelectronics
Question 3
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# ============================================================================
# Imports
# ============================================================================
from brian2 import *

# ============================================================================
# Set parameters
# ============================================================================
N = 50            # Number of neurons (used for simulating different currents)
E_L = -70 *mV     # Leak reversal potential
R_m = 10 * Mohm   # Membrane resistance
tau_m = 10 * ms   # Membrane time constant
V_th = -54 * mV   # Threshold potential
V_reset = -80 * mV  # Reset potential
duration = 500 * ms # Simulation duration

# ============================================================================
# Simulation
# ============================================================================

# Integrate-and-fire model equations
eqs="""
dv/dt = (E_L - v + (R_m*I_e)) / tau_m : volt
I_e = I_ext * int((t>100*ms) and (t<400*ms)) : amp
I_ext : amp
"""
# This equations will be executed after v hit the V_th
reset="""
v = V_reset
"""
# Making a group of neurons
G = NeuronGroup(N, model=eqs, method='euler', threshold='v>V_th', reset=reset)
# Setting initial values of v for each neurons
G.v = E_L
# Setting I_ext for each neuron
G.I_ext = '(10*nA) * i / N'
# Recording Spikes
spikemon = SpikeMonitor(G)
# Run Simulation
run(duration, report='stdout')
# Calculating firing rate from number of spikes per curent injection duration
rate_sim = (spikemon.count/(300*ms))/Hz
# Calculating firing rate from Eq(5.11)
rate_eq = 1 / (tau_m * log(((R_m*G.I_ext) + E_L - V_reset) / ((R_m*G.I_ext) + E_L - V_th)))

# ============================================================================
# Plots
# ============================================================================
figure()
plot(G.I_ext/nA, rate_sim)
plot(G.I_ext/nA, rate_eq)
xlabel('I_e (nA)')
ylabel('firing rate (Hz)')
legend(['Simulation', 'Equation'])
show()




