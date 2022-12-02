"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 5 : Model Neurons I: Neuroelectronics
Question 7
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
# Set Parameters
# ============================================================================
E_L = -70 *mV       # Leak reversal potential
V_th = -54 * mV     # Threshold
V_reset = -80 * mV  # Reset voltage
tau_m = 20 * ms     # Membrane time constant
r_mg_s = 0.15
P_max = 0.5
R_mI_e = 18 * mV
tau_s = 10 * ms

E_s = -80 * mV
# ============================================================================
# Simulation
# ============================================================================
eqs='''
dv/dt = (E_L - v - (r_mg_s*P_s*(v-E_s)) + R_mI_e) / tau_m : volt
dP_s/dt = (e*P_max*z - P_s) / tau_s : 1
dz/dt = -z/tau_s : 1
'''

G = NeuronGroup(2, eqs, method='euler', threshold='v>V_th', reset='v = V_reset') 

n1 = G[0]
n2 = G[1]

n1.v = -70 * mV
n2.v = -65 * mV


eqs_pre='''
z += 1
'''

S1 = Synapses(n1, n2, on_pre=eqs_pre)
S1.connect()

S2 = Synapses(n2, n1, on_pre=eqs_pre)
S2.connect()

run(3000*ms, report='stdout')
statemon = StateMonitor(G, ['v', 'P_s'], record=True)
spikemon = SpikeMonitor(G)

run(100*ms, report='stdout')


# ============================================================================
# Plots
# ============================================================================
figure()
subplot(2, 1, 1)
plot(statemon.t/ms, statemon.v[0, :]/mV, color='black')
for t in spikemon.spike_trains()[0]/ms:
    plt.vlines(t, ymin=-65, ymax=0, linestyles='solid', colors='black', lw = 1)
title('Inhibitory Synapses')
ylabel('V1 (mV)')
subplot(2, 1, 2)
plot(statemon.t/ms, statemon.v[1, :]/mV, color='black')
for t in spikemon.spike_trains()[1]/ms:
    plt.vlines(t, ymin=-65, ymax=0, linestyles='solid', colors='black', lw = 1)
xlabel('Time (ms)')
ylabel('V2 (mV)')
show()




