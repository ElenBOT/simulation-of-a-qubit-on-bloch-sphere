# -*- coding: utf-8 -*-
"""Create wave form. Mostly for I, Q signal.

In the realm of superconducting qubits, the input microwave signal sent into 
the qubit is not a sudden pulse wave but a pulse with padding. This padding is 
added to make the wave continuous, as the Fourier series of a wave overshoots
at points of finite discontinuity, known as 'the Gibbs phenomenon.'

The most common approach is the Gaussian padding or Lorentz padding, which use
Gaussian function and Lorentzian function.

function
----------
gaussian_padded_pulse
"""

import numpy as np
from matplotlib import pyplot as plt
__all__ = [
    'gaussian_padded_pulse'
]

def gaussian_padded_pulse(*,
                          t_on: float, 
                          sigma: float,
                          height: float, 
                          t_pad_ratio: float=3.5,
                          peak: bool=False):
    """Make a pulse wave with gaussian padding.
    
    Arguments
    ----------
    t_on : float
        The time when the pulse wave is at maximan.
    sigma : float
        The stander deviation of the gaussian function.
    height : float
        The height of the pulse wave.
    t_pad_ratio : float, optional
        The ratio between the time for padding and sigma. (default is 3)
        That is : t_pad = t_pad_ratio * sigma.
    peak : bool, optional
        If true, it'll plot the padded wave.
    
    Returns
    ----------
    waveform : callable(t)
        The padded pulse wave, t can be an 1d numpy.array or float.
    total_time : float
        The total time of pulse wave, include padding.
    """
    def gaussian(x, height, canter, sigma):
        """The 1D gaussian function with x be the variable."""
        return height * np.exp( -1/2 * (x-canter)**2 / sigma**2 )
    t_pad = t_pad_ratio * sigma
    total_time = t_on + 2*t_pad
    def waveform(t):
        if isinstance(t, np.ndarray):
            result = np.zeros_like(t)
            result[(0 <= t) & (t <= t_pad)] =\
                gaussian(t[(0 <= t) & (t <= t_pad)], height, t_pad, sigma)
            result[(t_pad < t) & (t < t_pad+t_on)] = height
            result[(t_pad+t_on <= t) & (t <= total_time)] =\
                gaussian(t[(t_pad+t_on <= t) & (t <= total_time)], 
                         height, t_pad+t_on, sigma)
            return result
        else: # is a constant
            if 0 <= t and t <= t_pad:
                return gaussian(t, height, t_pad, sigma)
            elif t_pad < t and t < t_pad+t_on:
                return height
            elif t_pad+t_on <= t and t <= total_time:
                return gaussian(t, height, t_pad + t_on, sigma)
            else: # assume what's outside is zero
                return 0
    if peak:
        samt = np.linspace(0, total_time, 200)
        plt.plot(samt * 1e+6, waveform(samt))
        plt.xlabel('$t/\\mu s$')
        plt.title('A peak of gaussian padded pulse')
        plt.show(block=True)
    return waveform, total_time
