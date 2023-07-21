# -*- coding: utf-8 -*-
"""Bloch Simulator

Provides and How To
  1. Set up an experiment scheme by providing a sequence of sections with 
     costimized physical quantities and duration.
  2. Numerically solve bloch equation for a given experiment scheme.
  3. Animate the time evolution of the solution or simply plot its trajectory
     on bloch sphere.
  4. Provide tool to make gaussian-padded pulse wave as a callable(t) that 
     returns a float.
  5. Provide a function that draw a bloch sphere and return its figure and axes
     for user to plot as desired.

It is advise to import this module as `bs`:

    import blochsimu as bs

To use this module, start off by providing default physical arguments 
throughout the experiment :

    phy_args = {
        'u0': (0.0, 0.0, 1.0),
        'z0': 1.0,
        'I' : 0,
        'Q' : 0,
        'd' : lambda t: 0,
        'G1': 1 / 85e-6,
        'G2': 1 / 120e-6,
    }

After this, we set up an experiment scheme by `bs.ExpScheme` class :

    expe = bs.ExpScheme(**phy_args)

Then use `bs.Section` to specify what experiment does. We can overwrite
some of the default physical argument and decide duration of each section :

    expe.sequence = (
        bs.Section(17e-6, I=1e+5), # pi/2 pluse of I
        bs.Section(80e-6 / 2),     # wait for tau/2
        bs.Section(40e-6, Q=1e+5), # pi pluse of Q
        bs.Section(80e-6 / 2),     # wait for tau/2
        bs.Section(17e-6, I=1e+5), # pi/2 pluse of I
    )

We can use the method `ExpScheme.plot_phy_arg` to have an overlook on
physical argument throughout the experiment :

    expe.plot_phy_arg('I', dt=5e-7, block=False)
    expe.plot_phy_arg('Q', dt=5e-7)

Then, we can numerically solve it by `bs.blochsolve` :

    u_sol, u_sol_section = bs.blochsolve(expe, dt=5e-7)

By `bs.blochdrawer`, we can animate it or simply plot the result :

    bs.blochdrawer.plot(u_sol, block=False)
    bs.blochdrawer.animate(u_sol, t_interval=1e-2)

The `waveform` module provide tools to make the gaussian padded pulse waves.
Which is commonly used in the experiment of superconducting qubits.

    pi_pulse, t_pipulse = bs.gaussian_padded_pulse(
        t_on=89e-7, sigma=10e-8, height=3.5e+5, peak=True)
    print(pi_pulse(t=10e-8))
    print(pi_pulse(np.linspace(0, 10e-8, 5)))

The `draw_bloch_sphere` function returns an figure and axes with a bloch 
sphere drawn on it.

    fig, ax = draw_bloch_sphere('Figure title')
    ax.plot(0.5, 0.5, 0.5, 'r o')
    plt.show()

For more detail, see docstring for each class method.

Classes
----------
  * ExpScheme -- An experiment setup scheme.
  * Section -- A section with customized physical argument and duration.

Class instance
----------
  * blochdrawer -- Animate or plot the quantum state on the bloch sphere.

Functions
----------
  * blochsolve -- numerically solve a given experiment scheme.
  * gaussian_padded_pulse -- Make a pulse wave with gaussian padding.
  * draw_bloch_sphere -- create a figre and axes with bloch sphere drawn.
"""

from .expscheme import Section, ExpScheme
from .blochnumint import blochsolve
from .blochdraw import blochdrawer, draw_bloch_sphere
from .waveform import gaussian_padded_pulse
