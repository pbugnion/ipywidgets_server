
import matplotlib.pyplot as plt

import numpy as np

import ipywidgets as widgets

XBASIS = np.linspace(-2*np.pi, 2*np.pi)


class SineRenderer(object):

    def __init__(self):
        self._amplitude_slider = widgets.FloatSlider(
            1.0, min=-2.0, max=2.0, description='amplitude'
        )
        self._frequency_slider = widgets.FloatSlider(
            1.0, min=0.1, max=3.0, description='frequency'
        )
        self._bind_callbacks()
        self._controls_container = widgets.VBox([
            self._amplitude_slider,
            self._frequency_slider
        ])
        self._plot_container = widgets.HBox([])
        self._application_container = widgets.HBox([
            self._controls_container, self._plot_container
        ])

    def _bind_callbacks(self):
        self._amplitude_slider.observe(
            self._on_param_change, names='value')
        self._frequency_slider.observe(
            self._on_param_change, names='value')

    def _on_param_change(self, change):
        self.render()

    def render(self, change=None):
        amplitude = self._amplitude_slider.value
        frequency = self._frequency_slider.value
        output = widgets.Output()
        with output:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.plot(XBASIS, amplitude * np.sin(frequency*XBASIS))
            ax.set_ylim(-2.5, 2.5)
            plt.show()
        self._plot_container.children = [output]
        return self._application_container


container = SineRenderer().render()
