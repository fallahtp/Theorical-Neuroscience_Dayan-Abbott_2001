"""
Answers to 'Theorical Neuroscience, Dayan-Abbott (2001)' exersises
Chapter 6 : Model Neurons II: Conductances and Morphology
Question 3
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
# Simulation
# ============================================================================
eqs="""
dv/dt = (v*(1-v**2) - u + I_e) * Hz : 1
du/dt = epsilon*(v-0.5*u) : 1
I_e : 1
epsilon : Hz
"""

G = NeuronGroup(4, model=eqs, method='rk2')
G.I_e = [0, 0, 0, -1]
G.epsilon = [0.3, 0.1, 1, 0.3] * Hz
G.v = -0.5

statemon = StateMonitor(G, ['v', 'u'], record=True)

run(40*second, report='stdout')

# ============================================================================
# Plots
# ============================================================================
figure()
plot(statemon.v[0, :], statemon.u[0, :])
plot(statemon.v[1, :], statemon.u[1, :])
plot(statemon.v[2, :], statemon.u[2, :])
xlabel('V')
ylabel('u')
legend(['epsilon = 0.3', 'epsilon = 0.1', 'epsilon = 1'])
title('Phase Plane (I_e = 0)')
#
figure()
plot(statemon.v[3, :], statemon.u[3, :])
xlabel('V')
ylabel('u')
title('Phase Plane (I_e = -1)')
#
figure()
plot(statemon.t, statemon.v[0, :])
plot(statemon.t, statemon.v[1, :])
plot(statemon.t, statemon.v[2, :])
xlabel('Time (Second)')
ylabel('V')
legend(['epsilon = 0.3', 'epsilon = 0.1', 'epsilon = 1'])
title('V (I_e = 0)')
#
figure()
plot(statemon.t, statemon.v[3, :])
xlabel('Time (Second)')
ylabel('V')
title('V (I_e = -1)')

show()

