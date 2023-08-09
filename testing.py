"""Examples of how you can use blochsimu.

In this python file, five examples are given, let code speaks for itself.
"""

import blochsimu as bs
from matplotlib import pyplot as plt
import numpy as np

phy_args = {
    'u0': (0.0, 0.0, 1.0),
    'z0': 1.0,
    'I' : 0,
    'Q' : 0,
    'd' : 0,
    'G1': 1 / 85,
    'G2': 1 / 120,
}
dt = 5e-4 # sampling time for numerical integral


# d  / x \   / -G2  -d   I\ / x \   /   0   \ 
#----| y | = |  d  -G2  -Q| | y | + |   0   |
# dt \ z /   \ -I   Q  -G1/ \ z /   \ G1*z0 /
# G is short for Gamma. 
# G1: relaxation
# G2: decoherence
# Gp: dephaseing
Gp = 0.5
G1 = 0.5
G2 = Gp + G1/2
# Note : I = 1.58 for 1s to achieve pi/2-pluse,
#        I = 1.58 for 2s to achieve pi-pluse
expe = bs.ExpScheme(**phy_args)
expe.sequence = (
    bs.Section(2, I=1.58), # pi pluse of I
    bs.Section(3, d=0, G1=G1, G2=0) # wait for qubit drops back to ground state.
)
u_sol1, u_sol_section1 = bs.blochsolve(expe, dt)
bs.blochdrawer.plot(u_sol1, block=True)