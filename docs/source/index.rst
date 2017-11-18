.. ipywidgets_server documentation master file, created by
   sphinx-quickstart on Sat Nov 18 09:28:24 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

IPywidgets server
=================

`IPywidgets server` lets you serve Jupyter widgets outside of a Jupyter
Notebook. Any Python callback defined on your widgets will work as in the
notebook.

Let's create a simple widget::

    # example.py

    from ipywidgets import IntSlider, Text, VBox
    s = IntSlider(max=200, value=100)
    t = Text()


    def update_text(change=None):
        t.value = str(float(s.value) ** 2)


    s.observe(update_text, names='value')
    update_text()
    vbox = VBox([s, t])

To serve this, just run the following, in the directory containing ``example.py``:

.. code-block:: bash

   $ ipywidgets-server example:vbox

This will serve the widget on ``http://localhost:8866/``:

.. image:: _images/simple-example.gif
