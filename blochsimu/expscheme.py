# -*- coding: utf-8 -*-
"""Setting up an experiment scheme by providing a sequence of sections.

This modual is used to set up an experiment scheme by providing a sequence of 
sections. Each sections contains costimized physical arguments and user
decided duration. The class `ExpScheme` creats an object to be the experiment 
scheme, while each section is an instance of the class `Section`.

For an experiment scheme, user must provide default value for each physical 
argument. Then, in each section, user can choose to overwrite some of them by
by providing key and value pair as keyword argument. The physical arguments
can be a function of time or a constant, achieved by python callable object or
a float.

Classes
----------
Section
ExpScheme
"""
import numpy as np
import numbers
from typing import Callable
from matplotlib import pyplot as plt
__all__ = [
    'Section', 
    'ExpScheme'
]

def _check_phyargs_input(phyargs: dict):
    """Check all physical arguments, they must be either be a callable or a number."""
    try:
        for key in ('I', 'Q', 'd', 'z0', 'G1', 'G2'):
            if (not callable(phyargs[key]) and
                not isinstance(phyargs[key],  numbers.Real)):  
                raise TypeError(key, phyargs[key])
    except TypeError as e:
        raise TypeError(
            f'The physical input for {e.args[0]}, {e.args[1]}, '
            + 'is not a callable nor a real number.') from None

class Section :
    """A section with customized physical argument and duration.
    
    Instance variable :
    ----------
    s : float
        The duration of this section, in seconds.
    phy_args : dictionary
        The physical arguments (I, Q, z0, d, G1, G2).
    expe : ExpScheme
        The experiment scheme this section belongs to.
    """

    def __init__(self, s: float, **phy_args) -> None:
        """Set duration, overwrite some(or None) of the default physical arguments.

        Argument
        ----------
        s : float
            The duration of this section.
            
        Keyword Argument
        ----------
        **phy_args :
            The physical arguments that overwrite default ones of the
            experiment scheme. The options : (I, Q, z0, d, G1, G2).
        """
        self.phy_args = phy_args
        self.s = s
        self.expe = None
    
    def _update_phy_args(self):
        """Update physical arguments.

        Set self.phy_args to be the default one of the experiment scheme.
        Then overwrite some of them accroding what user provide as keyword
        argument at __init__ constructor.
        """
        self.phy_args = {**self.expe.default_phy_args, **self.phy_args}
        _check_phyargs_input(self.phy_args)

    def __repr__(self):
        return f"A section with duration of {self.s*1e+6:.2f} us"


class ExpScheme:
    """An experiment setup scheme.

    Instance variable
    ----------
    sequence : list 
        A sequence of sections that describe what the experiment does.
    default_phy_args : dict
        Default physical arguments.
    u0 : numpy.ndarray with shape (3,)
        The inital position, with element [x0, y0, z0].
    fig : matplotlib.figure.Figure
        An Figure that is used to disaply physical argument plot.
    ax : matplotlib.axes._axes.Axes
        An axes object associate with self.fig, acess it to costimize
        the plotting.

    Public method
    ----------
    plot_phy_arg -- plot a physical quantity throughtout experiment.
    """

    def __init__(self, 
                 *,
                 u0: tuple[float] | list[float],
                 z0: Callable[[float], float] | float,
                 I: Callable[[float], float] | float,
                 Q: Callable[[float], float] | float,
                 d: Callable[[float], float] | float,
                 G1: Callable[[float], float] | float,
                 G2: Callable[[float], float] | float) -> None:
        """Set up an experiment scheme with default physical arguments.
        
        Keyword Arguments
        ----------
        u0 : tuple[floar] or list[float] with length 3.
            The inital position (x0, y0, z0).
        I  : callable(t) or float
            magnetic y config,
        Q  : callable(t) or float
            magnetic x config,
        z0 : callable(t) or float
            stable state z-component,
        d  : callable(t) or float
            detune,
        G1 : callable(t) or float
            relaxation rate,
        G2 : callable(t) or float
            decoherence rate.
        """
        if (not isinstance(u0, (tuple, list)) or
            len(u0) != 3):
            raise ValueError(
                'The input u0 (the initial position) should be a tuple '
                + 'or a list with length of 3.') from None 
        self.u0 = np.array(u0)
        self.default_phy_args = {
            'z0': z0, 'I': I, 'Q': Q,
            'd': d, 'G1': G1, 'G2': G2}
        _check_phyargs_input(self.default_phy_args)
        self._sequence = []
        self.total_time = 0
        self.fig = None
        self.ax = None

    def plot_phy_arg(self, phyarg_name: str, 
                     dt: float, *, 
                     mu_s_scale:bool=True,
                     show: bool=True,
                     block: bool=True) -> None:
        """plot a physical argument throught the entire experiment.

        Arguments
        ----------
        phyarg_name : string
            Used as key to acess the dictionary `phy_args`.
        dt : float
            The time interval for sampling (for plotting).
            
        Keyword Argument
        ----------
        mus_scale : bool, optional
            Plot time in micro second, default is True.
        show : bool, optional (default is True)
            If true, it'll call `matplotlib.pyplot.show()`, often renamed as 
            `plt.show()`. By set it to False, user can acess `self.ax` to 
            costimize the plotting, then manually call `plt.show()` afterwards.
        block : bool, optional (default is True)
            Block the program untill the figure is closed.
        """
        magnitude = []
        samt = []
        t_sofar = 0
        for act in self.sequence:
            goal = act.phy_args[phyarg_name]
            if callable(goal):
                samt_section = np.linspace(
                    t_sofar, act.s+t_sofar, int(act.s/dt))
                magnitude_section = [goal(t-t_sofar) for t in samt_section]
                samt = np.concatenate((samt, samt_section))
                magnitude = np.concatenate((magnitude, magnitude_section))
            else: # is constant
                samt_section = [t_sofar, act.s+t_sofar]
                samt = np.concatenate((samt, samt_section))
                magnitude =  np.concatenate((magnitude, [goal, goal]))
            t_sofar += act.s
        
        self.fig = plt.figure(phyarg_name)
        self.ax = self.fig.add_subplot(111)
        if mu_s_scale:
            self.ax.set_xlabel('$t/\\mu s$')
            self.ax.plot(samt * 1e+6, magnitude)
        else:
            self.ax.set_xlabel('$t/s$')
            self.ax.plot(samt, magnitude)
        if show: plt.show(block=block)

    @property
    def sequence(self):
        return self._sequence
    @sequence.setter
    def sequence(self, sections: tuple[Section] | list[Section]):
        """For each section, regist them to belong to this experiment scheme."""
        for section in sections :
            if not isinstance(section, Section):
                raise TypeError(
                    'The action in the sequecne should be the instance of the '
                    + 'class Section.') from None
            self.total_time += section.s
            section.expe = self
            section._update_phy_args()
        self._sequence = list(sections)

    def __repr__(self) -> str:
        title = 'An experiment setup with sequence :\n'
        contains = '\n'.join(repr(action) for action in self._sequence)
        return title + contains