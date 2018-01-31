
import time

import matplotlib.pyplot as plt

import numpy as np

import ipywidgets as widgets
from IPython.display import display

SIZE = 50
XBASIS = np.linspace(0.0, 1.0, SIZE)


container = widgets.VBox()


def update():
    output = widgets.Output()
    with output:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(XBASIS, np.random.rand(SIZE))
        ax.set_ylim(0.0, 1.0)
        plt.show()
    container.children = [output]


display(container)


while True:
    time.sleep(1)
    update()
