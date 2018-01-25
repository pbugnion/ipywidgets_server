
Tutorials
=========

..
   Simple widget
   -------------

   Think of something to put here.

Using IPywidget server with Matplotlib
--------------------------------------

Let's build a simple application that updates a matplotlib plot every second. We
use an ``Output`` widget to get capture the matplotlib plot. We then embed our
output widget in a top-level container. Every second, we generate a new output
widget containing a new plot and swap it into the container. The code for this
example is in `examples/matplotlib_simple`::

    # example.py

    import time

    import matplotlib.pyplot as plt

    import numpy as np

    import ipywidgets as widgets
    from IPython.display import display

    SIZE = 50
    XBASIS = np.linspace(0.0, 1.0, SIZE)


    container = widgets.VBox()


    def update():
        """ Generate a new random plot and embed it into the container """
        output = widgets.Output()
        with output:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.plot(XBASIS, np.random.rand(SIZE))
            ax.set_ylim(0.0, 1.0)
            plt.show()
        container.children = [output]


    display(container)


    while True:
        # Update the plot in a busy loop
        time.sleep(1)
        update()


Save this script to a file called `example.py`. You can then run::

    ipywidgets-server example:container

Head over to `http://127.0.0.1:8866` in your browser. You should see the widget.

.. image:: images/matplotlib-simple.png

For a more complex example, let's build a widget to explore how the `sin` changes
depending on the parameters that are passed. We will plot ``a * sin(k*x)``, with sliders to change the value of ``a`` and ``k``::

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

.. image:: images/matplotlib-sine.png

It is worth noting the following:

 - we wrap the application into a controller class responsible both for generating the view and for reacting to user actions. Using a class provides better encapsulation and re-use.
 - in the class constructor, we handle rendering the static components of the view. We create two container widgets, one to hold the sliders and one to hold the plot. We stack these two containers in an ``HBox``, the top level widget holding our application.
 - We handle reacting to changes in the sliders by `observing` the ``value`` traitlet of the slider. The ``.observe`` method takes a callback as first argument. The callback that we pass in just re-renders the plot. The second argument to ``.observe`` is a list of attributes of the slider to observe. We only want to react to changes in the slider value (rather than, say, its maximum or minimum).
 - The ``render`` method of our application renders the dynamic components and returns the top level widget.


..
   Creating widgets with bqplot
   ----------------------------

   Creating widgets with ipyvolume
   -------------------------------
