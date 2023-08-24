# -*- coding: utf-8 -*-
"""Animate and plot the time evolution of a quantum state on the Bloch sphere.

For a two-level quantum state discreble by bloch sphere with coordinate
u(t) = (x(t), y(t), z(t)). `blochdrawer` can plot or animate the time evolution
of u(t) on the Bloch sphere, by acppect an (3, N) numpy array that contains
discrete points that is dense enough to be seen as an animation or a trajectory.

The object `blochdrawer` is an instance of the class `BlochSphereDarwer`,
which we don't need to concern. The purpose of this class is to ensure the 
'matplotlib.animation.FuncAnimation' objects exists in every scope, thus 
allowing the animation to be displayed correctly by matplotlib.

For plotting, user can set the keyword argument `show = False` and acess
self.ax to costimize the plot. 

`draw_bloch_sphere` create an figure with bloch sphere drawn on it and return
its figure and axes, user can make use of it to plot anything as desired.


Class
----------
BlochSphereDarwer

Class instance
----------
blochdrawer

function
----------
draw_bloch_sphere
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.axes

__all__ = [
    'BlochSphereDarwer',
    'blochdrawer',
    'draw_bloch_sphere'
]

def draw_bloch_sphere(figure_title: str) -> tuple:
    """Create a figure, plot a bloch sphere and return its axes.
    
    Argument
    ----------
    figure_title : str
        The title of the figure, notice that duplicate name will overwrite
        previous figure.
    
    Returns
    ----------
    fig : matplotlib.figure.Figure
        An Figure that is used to disaply plot.
    ax : matplotlib.axes._axes.Axes
        An axes object associate with self.fig.
    """
    # creat figure and axes
    fig = plt.figure(figure_title)
    ax = fig.add_subplot(111, projection = '3d')
    ax.set(title = 'Qubit on bloch sphere')
    ax.set(xlim3d=(-1.1, 1.1), ylim3d=(-1.1, 1.1),
                zlim3d=(-1.1, 1.1))
    # plot spherical coordinate curves
    u, v = np.mgrid[0 : 2*np.pi : 200j, 0 : np.pi : 100j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, rstride=18, cstride=18, linewidth=1, color='tan')
    # add axis and labeling
    ax.quiver(-1.3,  0,  0, 2.6, 0, 0, color = 'k', arrow_length_ratio = 0.05) # x-axis
    ax.quiver( 0, -1.3,  0, 0, 2.6, 0, color = 'k', arrow_length_ratio = 0.05) # y-axis
    ax.quiver( 0,  0, -1.3, 0, 0, 2.6, color = 'k', arrow_length_ratio = 0.05) # z-axis
    ax.text( 1.5, 0, 0, '$x$',
            color='k', fontweight=100, fontsize=15,
            horizontalalignment='center', verticalalignment='center')
    ax.text( 0, 1.5, 0, '$y$',
            color='k', fontweight=100, fontsize=15,
            horizontalalignment='center', verticalalignment='center')
    ax.text( 0, 0, 1.5, '$|0\\rangle $',
            color='red', fontweight=400, fontsize=15,
            horizontalalignment='center', verticalalignment='center')
    ax.text( 0, 0,-1.5, '$|1\\rangle $',
            color='red', fontweight=400, fontsize=15,
            horizontalalignment='center', verticalalignment='center') 
    ax.axis('off')
    ax.set_box_aspect( [1, 1, 1] )
    return fig, ax

class BlochSphereDarwer:
    """
    Animate time evolution of a state on bloch sphere.
    
    Instance variables
    ----------
    u : numpy.ndarray with shape (3, N)
        a list of coordinates to be animated or plot. 
    fig : matplotlib.figure.Figure
        An Figure that is used to disaply plot and animation.
    ax : matplotlib.axes._axes.Axes
        An axes object associate with self.fig, acess it to costimize
        the plotting.

    Public methods
    ----------
    animate -- accpet a list of positions and display the animation.
    plot -- accpet a list of positions and plot the trajectory.
    """

    def plot(self, u: np.ndarray, 
             *, 
             sepe_N: int = 0,
             show: bool = True,
             block: bool =True
             ) -> None:
        """Plot the trajectory of the qubit.

        Arguments
        ----------
        u : numpy.ndarray with shape (4, N)
            The points to be plot.

        Keyword Arguments
        ----------
        sepe_N : int, optional (default is 0, it doesn't draw any marker)
            Plot a blue marker for every sepe_N points in the given positions. 
            In order to fell relative time scale of the time evolution.
        show : bool, optional (default is True)
            If true, it'll call `matplotlib.pyplot.show()`, often renamed as 
            `plt.show()`. By set it to False, user can acess `self.ax` to 
            costimize the plotting, then manually call `plt.show()` afterwards.
        block : bool, optional (default is True)
            Block the program untill the figure is closed.
        """
        if type(u) is not np.ndarray:
            raise TypeError(
                f'The input for u is not numpy.ndarray') from None
        if not u.shape[0] == 4:
            raise TypeError(
                f'The shape of u is {u.shape}, it should be (4, N)') from None
        u = u[1:4, :]
        self.fig, self.ax = draw_bloch_sphere('Qubit on bloch equation (plot)')
        self.ax.plot(*u, linewidth=5)
        self.ax.plot(*u[:, -1], 'ro')
        if sepe_N: self.ax.plot(*u[:, ::sepe_N], 'b o')
        if show: plt.show(block=block)

    def animate(self, u: np.ndarray, t_interval: float) -> None:
        '''Display the animation by accept a list of positions.
        
        Arguments
        ----------
        u : numpy.ndarray with shape (4, N)
            The points to be animate.
        t_interval : float
            The time interval between each fram of the animation, in seconds.
        '''
        if type(u) is not np.ndarray:
            raise TypeError(
                f'The input for u is not numpy.ndarray') from None
        if not u.shape[0] == 4:
            raise TypeError(
                f'The shape of u is {u.shape}, it should be (4, N)') from None
        u = u[1:4, :]
        
        self.fig, self.ax = draw_bloch_sphere('Qubit on bloch equation (animation)')
        t_interval = t_interval * 1000 # s --> ms
        
        def update_lines(num, datas, lines):
            for data in datas:
                # current state
                lines[0].set_data(data[0:2, num-1:num])
                lines[0].set_3d_properties(data[2, num-1:num])
                # trajectory
                lines[1].set_data(data[0:2, :num])
                lines[1].set_3d_properties(data[2, :num])
            return lines
        linobjs = [
            # plot current state (as a point on bloch sphere).
            self.ax.plot(*u, 'ro')[0],
            # plot trajectory
            self.ax.plot(*u, linewidth=3)[0]
        ]

        sam_num = u.shape[1]
        aniobj = matplotlib.animation.FuncAnimation(
            self.fig, update_lines, sam_num, fargs=([u], linobjs),
            interval=t_interval, blit=False, repeat=True, repeat_delay=1000)
        plt.show(block = True)

blochdrawer = BlochSphereDarwer()