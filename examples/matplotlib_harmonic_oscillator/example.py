
import numpy as np
from numpy.polynomial.hermite import Hermite
import matplotlib.pyplot as plt

import ipywidgets as widgets

from IPython.display import clear_output

MAX_POLY = 10

coeffs = [([0] * i) + [1] for i in range(MAX_POLY + 1)]

# Hermite polynomials up to MAX_POLY
polynomials = [Hermite(coeff) for coeff in coeffs]

slider = widgets.IntSlider(
    4, min=0, max=MAX_POLY, step=1, description=r'n'
)

label = widgets.Label()

plot_widget = widgets.Output()


def create_label_value(n):
    ordinal = 'th'
    if n == 1:
        ordinal = 'st'
    elif n == 2:
        ordinal = 'nd'
    elif n == 3:
        ordinal = 'rd'
    return '{}{} eigenfunction of the quantum harmonic oscillator'.format(
        n, ordinal)


def quantum_harmonic_oscillator_eigenfunction(n, x):
    prefactor = 1./np.sqrt((2.0**n * np.math.factorial(n)))
    poly = polynomials[n]
    return prefactor*poly(x)*np.exp(-0.5*x**2)


def on_slider_change(change=None):
    """
    When the slider changes, we:

     - destroy the plot
     - reset the label
     - draw the new function on top
    """
    n = slider.value
    label.value = create_label_value(n)
    with plot_widget:
        clear_output()
        startx = 2.0*np.sqrt(2*n+1)
        xbasis = np.linspace(-startx, startx, 100)
        plt.plot(
            xbasis,
            quantum_harmonic_oscillator_eigenfunction(n, xbasis)
        )
        plt.show()


slider.observe(on_slider_change, names='value')

on_slider_change()

vbox = widgets.VBox([slider, label, plot_widget])
