# -*- coding: utf-8 -*-
"""Solve bloch equation numericaly. 

For a two-level quantum system describe by bloch sphere with coordinate
u(t) = (x(t), y(t), z(t)). The equation of motion is the so called
"bloch equation", when writes in matrix form, it has expression:
 d  / x \   / -G2  -d   I\ / x \   /   0   \ 
----| y | = |  d  -G2  -Q| | y | + |   0   |
 dt \ z /   \ -I   Q  -G1/ \ z /   \ G1*z0 /
I  : magnetic y config,
Q  : magnetic x config,
z0 : stable state z-component,
d  : detune,
G1 : relaxation rate,
G2 : decoherence rate.

The function `blochsolve` accept an experiment scheme (the instance of `ExpScheme`)
as input, then it solves bloch equation numerically according to this experiment 
setup, returns an (3, N) numpy array that contains the numerical solution of u(t).

function
----------
blochsolve
"""

import numpy as np
from scipy.integrate import odeint
from .expscheme import Section, ExpScheme
from typing import Callable, Tuple
__all__ = [
    'blochsolve'
]

def _dudt(u: tuple,
          t: float,
          I_in: Callable[[float], float] or float,
          Q_in: Callable[[float], float] or float,
          d_in: Callable[[float], float] or float,
          z0_in: Callable[[float], float] or float,
          G1_in: Callable[[float], float] or float,
          G2_in: Callable[[float], float] or float) -> Tuple[float]: 
    '''
    A function used as an argument for scipy.integrate.odeint.

    Return the first derivitives of position, ruled by bloch equation :
     d  / x \   / -G2  -d   I\ / x \   /   0   \ 
    ----| y | = |  d  -G2  -Q| | y | + |   0   | 
     dt \ z /   \ -I   Q  -G1/ \ z /   \ G1*z0 / 

    Arguments 
    ----------
    u : tuple
        The position. 
        u[0] is the x-component.
        u[1] is the y-component.
        u[2] is the z-component.
    t : float
        time, the depedent varaible.
    I : callable(t) or float
        I, magnetic y config.
    Q : callable(t) or float
        Q, magnetic x config.
    d : callable(t) or float
        Detune.
    z0 : callable(t) or float
        Stable state z-component.
    G1 : callable(t) or float
        Relaxation rate.
    G2 : callable(t) or float
        decoherence rate.

    Returns 
    ----------
    dudt : tuple
        dudt[0] is the dx/dt,
        dudt[1] is the dy/dt,
        dudt[2] is the dz/dt.
    '''
    x, y, z = u
    I, Q, d, z0, G1, G2 = I_in, Q_in, d_in, z0_in, G1_in, G2_in
    if callable(I_in): I = I_in(t)
    if callable(Q_in): Q = Q_in(t)
    if callable(d_in): d = d_in(t)
    if callable(z0_in): z0 = z0_in(t)
    if callable(G1_in): G1 = G1_in(t)
    if callable(G2_in): G2 = G2_in(t)

    dxdt = -G2*x - d*y  + I*z  +   0
    dydt =  d*x  - G2*y - Q*z  +   0
    dzdt = -I*x  + Q*y  - G1*z + G1*z0
    dudt = dxdt, dydt, dzdt
    return dudt

def _numint_section(u0: float, duration: float, 
                    args: tuple, sam_num: int) -> np.ndarray:
    '''
    perform numerical integral of bloch equation.

    Arguments
    ----------
    u0 : numpy.ndarray with shape (3,)
        The inital position.
    duration : float
        The time of the integrated time interval.
    args : tuple
        = (I, Q, d, z0, G1, G2), the arguments for integration.
    sam_num : int
        The number of sampling points within the time interval.

    Returns 
    ----------
    u_sol : numpy.ndarray with shape (4, sam_num)
        The result of numerical integral.
        u_sol[0, n] is the n-th sampling time,
        u_sol[1, n] is the x-component of n-th sampling time,
        u_sol[2, n] is the y-component of n-th sampling time,
        u_sol[3, n] is the z-component of n-th sampling time.
    '''
    samt = np.linspace(0, duration, sam_num)
    u_sol = odeint(_dudt, u0, samt, args = args)
    u_sol = np.vstack([samt.reshape(1, -1), u_sol.T])
    return u_sol

def blochsolve(expe: ExpScheme, dt: float) -> Tuple[np.ndarray]:
    '''
    Solve a given experiment scheme.

    Arguments
    ----------
    expe : ExpScheme object
        The experiment scheme.
    dt : float
        The time interval for sampling in numerical integration.

    Returns
    ----------
    u_sol : numpy.ndarray with shape (4, N)
        The complete numerical solution of u(t) under the experiment setup.
        u_sol[0, n] is the n-th sampling time,
        u_sol[1, n] is the x-component of n-th sampling time,
        u_sol[2, n] is the y-component of n-th sampling time,
        u_sol[3, n] is the z-component of n-th sampling time.
    u_sol_sections : list
        A list contains numerical solutions of u(t) for each section in
        the experiment sheme. Each element in the list has the discription
        as u_sol above.
    '''
    u_sol_sofar = []
    t_sofar = 0
    for section in expe.sequence:
        t_sofar += section.s
        if len(u_sol_sofar) == 0:
            u_start = expe.u0
        else:
            u_start = u_sol_sofar[-1].T[-1, 1:4]
        sam_num = int(section.s / dt)
        args = (
            section.phy_args['I'],
            section.phy_args['Q'],
            section.phy_args['d'],
            section.phy_args['z0'],
            section.phy_args['G1'],
            section.phy_args['G2'],
        )
        u_sol_section = _numint_section(
            u_start, section.s, args, sam_num)
        u_sol_sofar.append(u_sol_section)
    
    u_sol_sections = tuple(u_sol_section for u_sol_section in u_sol_sofar)
    u_sol = np.hstack(u_sol_sofar)
    return u_sol, u_sol_sections
