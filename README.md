# blochsimu - a python module for qubit simulation
`blochsimu` is a light weight python module that provide easy ways to simulate and plot the behavior of a qubit on bloch sphere.

<a href="https://pypi.org/project/<package-name>"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/<package-name>"></a>

## Requirements
* python 3.7+
* numpy
* scipy
* matplotlib

## Provides
1. Set up an experiment scheme by providing a sequence of sections with costimized physical quantities and duration.
2. Numerically solve bloch equation for a given experiment scheme.
3. Animate the time evolution of the solution or simply plot its trajectory on bloch sphere.
4. Provide tool to make gaussian-padded pulse wave as a callable(t) that returns a float.
5. Provide a function that draw a bloch sphere and return its figure and axes for user to plot as desired.

## Install

1. Install from PyPI
    ```shell
    pip install <package-name>
    ```

1. Download the latest release from [Release v0.0.1](https://github.com/ElenBOT/simulation-of-a-qubit-on-bloch-sphere/releases/tag/v0.0.1)
    ```shell
    pip install <package-name>-v0.0.1.tar.gz
    ```

## Usage
It is advised to import this module as `bs`.
```
import blochsimu as bs
```
For examples, see `example.py` in the folder.