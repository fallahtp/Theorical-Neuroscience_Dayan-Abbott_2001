"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 6 : Model Neurons II: Conductances and Morphology
Question 2
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
Mahdi Fallah
https://github.com/fallahtp
fallahtp@gmail.com
"""

# ============================================================================
# Imports
# ============================================================================
from brian2 import *

# ============================================================================
# Setting Parameters
# ============================================================================
g_L = 0.005 * mS/mm2
g_Ca = 0.01 * mS/mm2
g_K = 0.02 * mS/mm2
E_L = -50 * mV
E_Ca = 100 * mV
E_K = -70 * mV
c_m = 10 * nF/mm2

# ============================================================================
# Simulation
# ============================================================================
eqs="""
dv/dt = (-i_m + I_e)/c_m : volt

I_e : amp/meter**2

i_m = g_L*(v-E_K) +
      g_Ca*Minf*(v-E_Ca) + 
      g_K*n*(v-E_K) : amp/meter**2

Minf = 1/(1+exp(-0.133*(v/mV+1))) : 1

dn/dt = (ninf - n)/tau_n : 1
tau_n = (3/cosh(0.0345*(v/mV - 10))) * ms : second
ninf = (1/(1 + exp(-0.138*(v/mV - 10)))) : 1
"""

N = 100 # Number of neurons
duration = 100 * ms
I_max = 500.0 * namp/mm2

G = NeuronGroup(N, model=eqs, method='exponential_euler', threshold='v>-40*mV')
G.v = -70 * mV
G.I_e = 'I_max*i/N'

statemon = StateMonitor(G, ['v', 'n', 'I_e'], record=True)
spikemon = SpikeMonitor(G, record=True)

run(duration, report='stdout')

rate = spikemon.count / duration
I_th = statemon.I_e[(nonzero(rate)[0][0]), 0]

# ============================================================================
# Plot
# ============================================================================
plot(statemon.I_e[:, 0]/I_th, rate/Hz)
xlabel('I/I_threshold')
ylabel('Firing rate (Hz)')
#
figure()
plot(statemon.t/ms, statemon.v[50, :]/mV)
xlabel('Time (ms)')
ylabel('V (mV)')
title('V for neuron number 50')
#
figure()
plot(statemon.t/ms, statemon.n[50, :])
xlabel('Time (ms)')
ylabel('N')
title('N for neuron number 50')
#
figure()
plot(statemon.v[50, :], statemon.n[50, :])
xlabel('V')
ylabel('N')
title('Phase plane for neuron number 50')

show()

