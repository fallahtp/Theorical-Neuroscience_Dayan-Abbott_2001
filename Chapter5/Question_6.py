"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 5 : Model Neurons I: Neuroelectronics
Question 6
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
eqs_1="""
dv/dt = (E_L - v + (R_m*I_e) - I_syn) / tau_m : volt
I_e = 0 * nA : amp
I_syn = r_mg_s*P_s*(v-E_s) : volt
dP_s/dt = (e*P_max*z - P_s) / tau_s : 1
dz/dt = -z/tau_s : 1
"""
eqs_2="""
dv/dt = (E_L - v + (R_m*I_e) - I_syn) / tau_m : volt
I_e = 0 * nA : amp
I_syn = r_mg_s*P_s*(v-E_s) : volt
dP_s/dt = (e*P_max*z*(1-P_s) - P_s) / tau_s : 1
dz/dt = -z/tau_s : 1
"""

# This equations will be executed after v hit the V_th
reset="""
v = V_reset
"""
# Making a group of neurons
G1 = NeuronGroup(N, model=eqs_1, threshold='v>V_th', reset=reset)
G2 = NeuronGroup(N, model=eqs_2, threshold='v>V_th', reset=reset)
# Setting initial values of v for each neurons
G1.v = E_L
G2.v = E_L

# Making a spike generator to spike in the given times
rate = 100
num_spike = int(duration * rate /(1*second))
indeces = arange(0, num_spike, 1)
times = linspace(0, int(duration/ms), num_spike) * ms
PG = SpikeGeneratorGroup(num_spike, indeces, times=times)

# This equation will be executed after presynaptic spike arrives
eqs_pre="""
z += 1
"""
# Creating synapses between spike generator and our neuron
S1 = Synapses(PG, G1, on_pre=eqs_pre)
S1.connect()

S2 = Synapses(PG, G2, on_pre=eqs_pre)
S2.connect()

# Recording V, Synaprinc current and P_s
statemon1 = StateMonitor(G1, ['v', 'I_syn', 'P_s'], record=True)
statemon2 = StateMonitor(G2, ['v', 'I_syn', 'P_s'], record=True)

# Run Simulation
run(duration, report='stdout')

# ============================================================================
# Plots
# ============================================================================
figure('Equation 5')
subplot(3, 1, 1)
plot(statemon1.t/ms, statemon1.v[0, :]/mV)
ylabel('V (mV)')
subplot(3, 1, 2)
plot(statemon1.t/ms, -statemon1.I_syn[0, :]/mV)
ylabel('I_syn (mV)')
subplot(3, 1, 3)
plot(statemon1.t/ms, statemon1.P_s[0, :])
xlabel('Time (ms)')
ylabel('P_s')
#
figure('Equation 6')
subplot(3, 1, 1)
plot(statemon2.t/ms, statemon2.v[0, :]/mV)
ylabel('V (mV)')
subplot(3, 1, 2)
plot(statemon2.t/ms, -statemon2.I_syn[0, :]/mV)
ylabel('I_syn (mV)')
subplot(3, 1, 3)
plot(statemon2.t/ms, statemon2.P_s[0, :])
xlabel('Time (ms)')
ylabel('P_s')

show()
