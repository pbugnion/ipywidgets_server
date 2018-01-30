
Developing `ipywidgets-server`
==============================

Installation
------------

To develop `ipywidgets-server`, clone the `repository <https://github.com/pbugnion/widgets_server>`_ using git. Then, go into the project root and run::

    pip install -e .

This will build the JavaScript and install the Python in `editable mode <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_.

If you make changes to the ``js/`` directory, you will need to rebuild the frontend::

    cd js/
    npm run build

You will then need to refresh any open browser pages that contain `ipywidgets-server` instances. If you are making many changes to the JavaScript, you can build the frontend for every change with::

    npm run build:watch

If you make changes to the Python side, you will need to restart running `ipywidgets-server` instances. If you make changes to the `static` directory, you just need to refresh the browser page.

Running in debug mode
---------------------

You can run `ipywidget-server` in debug mode with::

    ipywidgets-server example:widget --WidgetsServer.log_level=DEBUG

You may also want to increase the log-level of the kernel driver. For this, change the log level in ``ipywidgets_server/kernel/__main__.py``.
