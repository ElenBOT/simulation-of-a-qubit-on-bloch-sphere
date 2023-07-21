"""Examples of how you can use blochsimu.

In this python file, five examples are given, let code speaks for itself.
"""
example = [
    'pulse_test', # 0
    'relaxation', # 1
    'echo', # 2
    'Ramsey', # 3
    'echo time domain', # 4
    'Ramsey time domain' # 5
][1]

import blochsimu as bs
from matplotlib import pyplot as plt
import numpy as np

phy_args = {
    'u0': (0.0, 0.0, 0.5),
    'z0': 1.0,
    'I' : 0,
    'Q' : 0,
    'd' : 0,
    'G1': 1 / 85e-6,
    'G2': 1 / 120e-6,
}
dt = 1e-8 # sampling time for numerical integral

pi_pulse, t_pipulse = bs.gaussian_padded_pulse(
    t_on=90e-7, sigma=10e-8, height=3.5e+5, peak=False)
pihalf_pulse, t_pihalfpulse = bs.gaussian_padded_pulse(
    t_on=43e-7, sigma=10e-8, height=3.5e+5)

def pulse_test(type_):
    test = bs.ExpScheme(**phy_args)
    if type_ == 'pi':
        test.sequence = (bs.Section(t_pipulse, I=pi_pulse),)
    if type_ == 'pi/2':
        test.sequence = (bs.Section(t_pihalfpulse, I=pihalf_pulse),)
    u_sol, _ = bs.blochsolve(test, dt)
    bs.blochdrawer.plot(u_sol)


if example == 'pulse_test':
    pulse_test('pi')
if example == 'relaxation':
    expe1 = bs.ExpScheme(**phy_args)
    expe1.sequence = (
        bs.Section(t_pipulse, I=pi_pulse), # pi pluse of I
        bs.Section(400e-6, d=0) # wait for qubit drops back to ground state.
    )
    detune = 2e+5
    expe2 = bs.ExpScheme(**phy_args)
    expe2.sequence = (
        bs.Section(t_pipulse, I=pi_pulse, d=0), # pi pluse of I
        bs.Section(400e-6, d=detune) # wait for qubit drops back to ground state.
    )
    u_sol1, u_sol_section1 = bs.blochsolve(expe1, dt)
    u_sol2, u_sol_section2 = bs.blochsolve(expe2, dt)
    
    # plot the z-component after the pi-pulse
    plt.figure("z-component after the pi-pulse")
    plt.plot(1e+6 * np.linspace(0, expe1.sequence[1].s, len(u_sol_section1[1][2,:])),
             u_sol_section1[1][2,:], 'r')
    plt.plot(1e+6 * np.linspace(0, expe2.sequence[1].s, len(u_sol_section2[1][2,:])),
             u_sol_section2[1][2,:], 'g')
    plt.xlabel('$t/\\mu s$')
    plt.show(block=True)
    # animate and plot whole process
    bs.blochdrawer.plot(u_sol1, block=True)
    bs.blochdrawer.plot(u_sol2, block=True)
    #bs.blochdrawer.animate(u_sol, 1e-2)
if example == 'echo':
    tau = 40e-6
    expe = bs.ExpScheme(**phy_args)
    expe.sequence = (
        bs.Section(t_pihalfpulse, I=pihalf_pulse), # pi/2 pluse of I
        bs.Section(tau / 2),                       # wait for tau/2
        bs.Section(t_pipulse, I=pi_pulse),         # pi pluse of Q
        bs.Section(tau / 2),                       # wait for tau/2
        bs.Section(t_pihalfpulse, I=pihalf_pulse), # pi/2 pluse of I
    )
    expe.plot_phy_arg('Q', dt, block=False)
    expe.plot_phy_arg('I', dt, block=True)
    u_sol, u_sol_section = bs.blochsolve(expe, dt)
    bs.blochdrawer.plot(u_sol, block=False)
    bs.blochdrawer.animate(u_sol, 1e-2)
if example == 'Ramsey':
    tau = 210e-6
    expe = bs.ExpScheme(**phy_args)
    expe.sequence = (
    bs.Section(t_pihalfpulse, I=pihalf_pulse), # pi/2 pulse
    bs.Section(tau),                                # wait tau
    bs.Section(t_pihalfpulse, I=pihalf_pulse)  # pi/2 pulse
    )
    u_sol, u_sol_section = bs.blochsolve(expe, dt)
    bs.blochdrawer.plot(u_sol, block=True)
    #bs.blochdrawer.animate(u_sol, 1e-2)
if example == 'echo time domain':
    taus = np.linspace(5e-6, 400e-6, 40)
    expes = []
    for tau in taus:
        expe = bs.ExpScheme(**phy_args)
        expe.sequence = (
            bs.Section(t_pihalfpulse, I=pihalf_pulse), # pi/2 pluse of I
            bs.Section(tau / 2),                       # wait for tau/2
            bs.Section(t_pipulse, I=pi_pulse),         # pi pluse of Q
            bs.Section(tau / 2),                       # wait for tau/2
            bs.Section(t_pihalfpulse, I=pihalf_pulse), # pi/2 pluse of I
        )
        expes.append(expe)
    z_end = []
    for expe in expes:
        u_sol, _ = bs.blochsolve(expe, dt)
        z_end.append(u_sol[2, -1])
    plt.figure('echo time domain')
    plt.plot(taus * 1e+6, z_end, 'k s')
    plt.xlabel(r'$\tau /\mu s$')
    plt.show()
if example == 'Ramsey time domain':
    taus = np.linspace(5e-6, 80e-6, 200)
    expes = []
    for tau in taus:
        expe = bs.ExpScheme(**phy_args)
        expe.sequence = (
            bs.Section(t_pihalfpulse, I=pihalf_pulse), # pi/2 pulse
            bs.Section(tau),                           # wait tau
            bs.Section(t_pihalfpulse, I=pihalf_pulse)  # pi/2 pulse
        )
        expes.append(expe)
    z_end = []
    for expe in expes:
        u_sol, _ = bs.blochsolve(expe, dt)
        z_end.append(u_sol[2, -1])
    plt.figure('Ramsey time domain')
    plt.plot(taus * 1e+6, z_end)
    plt.xlabel(r'$\tau /\mu s$')
    plt.show()