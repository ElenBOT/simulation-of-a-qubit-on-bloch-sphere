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
option = (
    'Ramesy once',        # 0
    'Ramesy time domain', # 1
    'Echo once',          # 2
    'Echo time domain'    # 3
)[3]
dt = 1e-7 # sampling time for numerical integral
if option == 'Ramesy once':
    tau = 30e-6
    delta = 0.1e+6
    expe = bs.ExpScheme(**phy_args)
    expe.sequence = (
        bs.Section(s=2.2e-6, I=7e+5, d = delta),
        bs.Section(s=tau, d = delta),
        bs.Section(s=2.2e-6, I=7e+5, d = delta),
    )
    u_sol, u_sol_section = bs.blochsolve(expe, dt)
    bs.blochdrawer.plot(u_sol, block=True)
if option == 'Ramesy time domain':
    taus = np.linspace(1e-6, 400e-6, 201)
    delta = 0.1e+6
    z_end = []
    for tau in taus:
        expe = bs.ExpScheme(**phy_args)
        expe.sequence = (
            bs.Section(s=2.2e-6, I=7e+5, d = delta),
            bs.Section(s=tau, d = delta),
            bs.Section(s=2.2e-6, I=7e+5, d = delta),
        )
        u_sol, u_sol_section = bs.blochsolve(expe, dt)
        z_end.append(u_sol[3, -1])

    plt.figure()
    plt.plot(taus*1e+6, z_end, 'k .')
    plt.title(r'Ramsey exepriment')
    plt.xlabel(r'$\tau$/us')
    plt.ylabel(r'$z$')
    plt.grid()
    plt.show()
if option == 'Echo once':
    tau = 30e-6
    delta = 0
    expe = bs.ExpScheme(**phy_args)
    expe.sequence = (
        bs.Section(s=2.2e-6, I=7e+5, d = delta),
        bs.Section(s=tau/2, d = delta),
        bs.Section(s=4.4e-6, I=7e+5, d = delta),
        bs.Section(s=tau/2, d = delta),
        bs.Section(s=2.2e-6, I=7e+5, d = delta),
    )
    u_sol, u_sol_section = bs.blochsolve(expe, dt)
    bs.blochdrawer.plot(u_sol, block=True)
if option == 'Echo time domain':
    taus = np.linspace(1e-6, 400e-6, 201)
    delta = 0
    z_end = []
    for tau in taus:
        expe = bs.ExpScheme(**phy_args)
        expe.sequence = (
            bs.Section(s=2.2e-6, I=7e+5, d = delta),
            bs.Section(s=tau/2, d = delta),
            bs.Section(s=4.4e-6, I=7e+5, d = delta),
            bs.Section(s=tau/2, d = delta),
            bs.Section(s=2.2e-6, I=7e+5, d = delta),
        )
        u_sol, u_sol_section = bs.blochsolve(expe, dt)
        z_end.append(u_sol[3, -1])

    plt.figure()
    plt.plot(taus*1e+6, z_end, 'k .')
    plt.title(r'Echo exepriment')
    plt.xlabel(r'$\tau$/us')
    plt.ylabel(r'$z$')
    plt.grid()
    plt.show()
