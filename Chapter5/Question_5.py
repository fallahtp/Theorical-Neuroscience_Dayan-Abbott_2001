"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 5 : Model Neurons I: Neuroelectronics
Question 5
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
N = 1             # Number of neurons
E_L = -70 *mV     # Leak reversal potential
R_m = 10 * Mohm   # Membrane resistance
tau_m = 10 * ms   # Membrane time constant
V_th = -54 * mV   # Threshold potential
V_reset = -80 * mV  # Reset potential
duration = 500 * ms # Simulation duration
E_s = 0 * mV        # Synaptic reversal potential
r_mg_s = 0.5        # r_m * g_s
tau_s = 10 * ms     # Synaptic time constant
P_max = 0.5

# ============================================================================
# Simulation
# ============================================================================

# Integrate-and-fire model equations pluse a synapse
eqs="""
dv/dt = (E_L - v + (R_m*I_e) - I_syn) / tau_m : volt
I_e = 0 * nA : amp
I_syn = r_mg_s*P_s*(v-E_s) : volt
dP_s/dt = (e*P_max*z - P_s) / tau_s : 1
dz/dt = -z/tau_s : 1
"""
# This equations will be executed after v hit the V_th
reset="""
v = V_reset
"""
# Making a group of neurons
G = NeuronGroup(N, model=eqs, method='euler', threshold='v>V_th', reset=reset)
# Setting initial values of v for each neurons
G.v = E_L

# Making a spike generator to spike in the given times
indeces = arange(0, 7, 1)
times = [50, 150, 190, 300, 320, 400, 410] * ms
SP = SpikeGeneratorGroup(7, indeces, times=times)

# This equation will be executed after presynaptic spike arrives
eqs_pre="""
z += 1
"""
# Creating synapses between spike generator and our neuron
S = Synapses(SP, G, on_pre=eqs_pre)
S.connect()

# Recording V, Synaprinc current and P_s
statemon = StateMonitor(G, ['v', 'I_syn', 'P_s'], record=True)

# Run Simulation
run(duration, report='stdout')

# ============================================================================
# Plots
# ============================================================================
figure()
subplot(3, 1, 1)
plot(statemon.t/ms, statemon.v[0, :]/mV)
ylabel('V (mV)')
subplot(3, 1, 2)
plot(statemon.t/ms, -statemon.I_syn[0, :]/mV)
ylabel('I_syn (mV)')
subplot(3, 1, 3)
plot(statemon.t/ms, statemon.P_s[0, :])
xlabel('Time (ms)')
ylabel('P_s')
show()




