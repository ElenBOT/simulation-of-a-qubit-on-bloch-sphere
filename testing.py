import blochsimu as bs
from matplotlib import pyplot as plt
import numpy as np


# d  / x \   / -G2  -d   I\ / x \   /   0   \ 
#----| y | = |  d  -G2  -Q| | y | + |   0   |
# dt \ z /   \ -I   Q  -G1/ \ z /   \ G1*z0 /
# default physical arguments:
G1 = 1 / 85e-6 
G2 = 1 / 150e-6
phy_args = {
    'u0': (0, 0, 1),
    'z0': 1.0,
    'I' : 0,
    'Q' : 0,
    'd' : 0,
    'G1': G1,
    'G2': G2,
}
d = 4e+6
option = (
    'once',
    'time domain'
)[0]
dt = 1e-8 # sampling time for numerical integral
if option == 'once':
    expe = bs.ExpScheme(**phy_args)
    expe.sequence = (
    bs.Section(s=5e-6, I=8e+6, d = d),
    )
    u_sol, u_sol_section = bs.blochsolve(expe, dt)
    bs.blochdrawer.plot(u_sol, block=False)
    plt.figure()
    plt.plot(u_sol[0, :]*1e+6, u_sol[3, :])
    plt.title(r'Rabi with large input power')
    plt.xlabel(r'$\tau$/us')
    plt.ylabel(r'$z$')
    plt.show()
if option == 'time domain':
    taus = np.linspace(1e-6, 300e-6, 100)
    zend = []
    for tau in taus:
        rasmsy = bs.ExpScheme(**phy_args)
        rasmsy.sequence = (
            bs.Section(s=12e-6, I=1e+5, d = d),
            bs.Section(s=tau, d = d),
            bs.Section(s=12e-6, I=1e+5, d = d),
        )
        u_sol, u_sol_section = bs.blochsolve(rasmsy, dt)
        zend.append(u_sol[2, -1])

    bs.blochdrawer.plot(u_sol, show=False)
    bs.blochdrawer.ax.view_init(elev=30, azim=45)
    plt.show(block = False)

