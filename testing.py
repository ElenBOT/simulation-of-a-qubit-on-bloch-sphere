import blochsimu as bs
from matplotlib import pyplot as plt
import numpy as np
dt = 5e-9 # sampling time for numerical integral

# d  / x \   / -G2  -d   I\ / x \   /   0   \ 
#----| y | = |  d  -G2  -Q| | y | + |   0   |
# dt \ z /   \ -I   Q  -G1/ \ z /   \ G1*z0 /
# default physical arguments:
def cir(x, y):
    return np.sqrt(1-x**2-y**2)
def cirx(x):
    return np.sqrt(1-x**2)
x, y, z = -0.15, +0.3, 0.3
phy_args = {
    'u0': (0, 0, 1),
    'z0': 1.0,
    'I' : 0,
    'Q' : 0,
    'd' : 0,
    'G1': 0,
    'G2': 0,
}
# G is short for Gamma. 
# G1: relaxation
# G2: decoherence
# Gp: dephaseing
G1 = 1 / 85e-6 
G2 = 1 / 150e-6
d = 8e+4
expe = bs.ExpScheme(**phy_args)

# taus = np.linspace(1e-6, 300e-6, 100)
# zend = []
# for tau in taus:
#     rasmsy = bs.ExpScheme(**phy_args)
#     rasmsy.sequence = (
#         bs.Section(s=12e-6, I=1e+5, d = d),
#         bs.Section(s=tau, d = d),
#         bs.Section(s=12e-6, I=1e+5, d = d),
#     )
#     u_sol, u_sol_section = bs.blochsolve(rasmsy, dt)
#     zend.append(u_sol[2, -1])

#bs.blochdrawer.plot(u_sol, show=False)
#bs.blochdrawer.ax.view_init(elev=30, azim=45)
#plt.show(block = False)
#z = u_sol[2, :]

expe.sequence = (
    bs.Section(s=24e-6, I=1e+5, d = d),
    bs.Section(s=400e-6, G1=G1, G2=G2, d = d),
)
u_sol, u_sol_section = bs.blochsolve(expe, dt)
bs.blochdrawer.plot(u_sol)