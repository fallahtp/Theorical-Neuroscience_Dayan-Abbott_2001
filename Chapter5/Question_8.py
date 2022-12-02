"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 5 : Model Neurons I: Neuroelectronics
Question 8
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
E_L = -54.387 * mV       # Leak reversal potential [mV]
E_K = -77 * mV           # Potassium reversal potential [mV]
E_Na = 50 * mV           # Sodium reversal potential [mV]
g_L = 0.003 * mS*mm**-2          # Leak Maximal Conductance
g_K = 0.36 * mS*mm**-2           # Potassium Maximal Conductance
g_Na = 1.2 * mS*mm**-2           # Sodium Maximal Conductance
c_m = 10 * nfarad * mmeter**-2    # Membrane Capacitance
defaultclock = 0.1 * ms
I_ext = TimedArray([-50, 0, 0, 0] *  namp * mm**-2, dt = 5*ms)
duration = 20 * ms      # Simulation Duration

# ============================================================================
# Simulation
# ============================================================================
eqs = """
dv/dt = (-i_m + I_e) / c_m : volt

I_e = I_ext(t) : amp * meter**-2
i_m = g_L*(v-E_L) + g_K*(n**4)*(v-E_K) + g_Na*(m**3 * h)*(v-E_Na) : amp * meter**-2

dn/dt = alpha_n*(1-n) - beta_n*(n) : 1
dm/dt = alpha_m*(1-m) - beta_m*(m) : 1
dh/dt = alpha_h*(1-h) - beta_h*(h) : 1

alpha_n = (0.01*(v/mV+55)) / (1 - exp(-0.1*(v/mV+55))) /ms : Hz
beta_n = 0.125*exp(-0.0125*(v/mV + 65)) /ms : Hz

alpha_m = (0.1*(v/mV+40)) / (1 - exp(-0.1*(v/mV+40))) /ms : Hz
beta_m = 4*exp(-0.0556*(v/mV + 65)) /ms : Hz

alpha_h = 0.07*exp(-0.05*(v/mV + 65)) /ms : Hz
beta_h = 1 / (1 + exp(-0.1*(v/mV+35))) /ms : Hz
"""
# Making Neuron Group
G = NeuronGroup(1, eqs, method='exponential_euler')
# Initial values
G.v = -65 * mV                   # This initial value is chosen with setting I_e = 0 and finding the steady state v.
G.n = 0.3177   # This value is steady state of n
G.m = 0.0529   # This value is steady state of m
G.h = 0.5961   # This value is steady state of h
# Motitors
statemon = StateMonitor(G, ['v', 'n', 'm', 'h', 'I_e'], record=0)
# spikemon = SpikeMonitor(G)     # If you want to record spikes you should define threshold in your NeuronGroup

run(duration, report='stdout')

# ============================================================================
# Plots
# ============================================================================
figure()
subplot(5, 1, 1)
plot(statemon.t/ms, statemon.v[0]/mV)
xticks([])
ylabel('V (mV)')
#
subplot(5, 1, 2)
plot(statemon.t/ms, statemon.I_e[0])
xticks([])
ylabel('I_e (A/m^2)')
#
subplot(5, 1, 3)
plot(statemon.t/ms, statemon.n[0])
xticks([])
ylabel('n')
#
subplot(5, 1, 4)
plot(statemon.t/ms, statemon.m[0])
xticks([])
ylabel('m')
#
subplot(5, 1, 5)
plot(statemon.t/ms, statemon.h[0])
xlabel('Time (ms)')
ylabel('h')
#
figure()
plot(statemon.t/ms, statemon.v[0]/mV)
xlabel('Time (ms)')
ylabel('V (mV)')

show()
