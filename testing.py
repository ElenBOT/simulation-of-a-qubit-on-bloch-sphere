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
d = 0.2e+6
option = (
    'cc',
    'once',
    'time domain'
)[1]
dt = 5e-7 # sampling time for numerical integral
if option == 'cc':
    bs.gaussian_padded_pulse(t_on=10e-6, 
                             sigma=1e-6, 
                             height=1, 
                             peak=True)
if option == 'once':
    expe = bs.ExpScheme(**phy_args)
    tau = 250e-6
    expe.sequence = (
        bs.Section(s=300e-6, I=7e+4, d = 1e+5),
    )
    u_sol, u_sol_section = bs.blochsolve(expe, dt)
    bs.blochdrawer.plot(u_sol, block=True)
    # plt.figure()
    # plt.plot(u_sol[0, :]*1e+6, u_sol[3, :])
    # plt.title(r'Rabi with large input power, detune = 0.4MHz')
    # plt.xlabel(r'$\tau$/us')
    # plt.ylabel(r'$z$')
    # plt.show()
if option == 'time domain':
    taus = np.linspace(1e-6, 400e-6, 201)
    zend1 = []
    zend2 = []
    for tau in taus:
        expe1 = bs.ExpScheme(**phy_args)
        expe1.sequence = (
            bs.Section(s=0.2e-6, I=8e+6, d = 0, G1=0),
            bs.Section(s=tau/2, d = 0, G1=0),
            bs.Section(s=0.4e-6, I=8e+6, d = 0, G1=0),
            bs.Section(s=tau/2, d = 0, G1=0),
            bs.Section(s=0.2e-6, I=8e+6, d = 0, G1=0),
        )
        u_sol1, u_sol_section1 = bs.blochsolve(expe1, dt)
        zend1.append(u_sol1[3, -1])

        expe2 = bs.ExpScheme(**phy_args)
        expe2.sequence = (
            bs.Section(s=0.2e-6, I=8e+6, d = 0),
            bs.Section(s=tau/2, d = 0),
            bs.Section(s=0.4e-6, I=8e+6, d = 0),
            bs.Section(s=tau/2, d = 0),
            bs.Section(s=0.2e-6, I=8e+6, d = 0),
        )
        u_sol2, u_sol_section2 = bs.blochsolve(expe2, dt)
        zend2.append(u_sol2[3, -1])


    plt.figure()
    plt.plot(taus*1e+6, zend1, 'r .', label='$\\Gamma_1=0$')
    plt.plot(taus*1e+6, zend2, 'k .', label='$\\Gamma_1=1/(85us)$')
    plt.title(r'Echo exepriment')
    plt.xlabel(r'$\tau$/us')
    plt.ylabel(r'$z$')
    plt.grid()
    plt.legend()
    plt.show()

