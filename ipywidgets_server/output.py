
from ipywidgets import DOMWidget

import sys
from traitlets import Unicode, Bool, Tuple
from IPython.display import clear_output


class Output(DOMWidget):
    """Widget used as a context manager to display output.

    This widget can capture and display stdout, stderr, and rich output.  To use
    it, create an instance of it and display it.  Then use it as a context
    manager.  Any output produced while in it's context will be captured and
    displayed in it instead of the standard output area.

    Example::
        import ipywidgets as widgets
        from IPython.display import display
        out = widgets.Output()
        display(out)

        print('prints to output area')

        with out:
            print('prints to output widget')
    """
    _view_name = Unicode('OutputView').tag(sync=True)
    _model_name = Unicode('OutputModel').tag(sync=True)
    _view_module = Unicode('ipywidgets_server/output').tag(sync=True)
    _model_module = Unicode('ipywidgets_server/output').tag(sync=True)
    is_capturing = Bool(
        False,
        help='Is the output widget currently capturing output.'
    ).tag(sync=True)
    outputs = Tuple(help='The output messages synced from the frontend.').tag(sync=True)

    def clear_output(self, *pargs, **kwargs):
        with self:
            clear_output(*pargs, **kwargs)

    def __enter__(self):
        """Called upon entering output widget context manager."""
        self._flush()
        self.is_capturing = True

    def __exit__(self, etype, evalue, tb):
        """Called upon exiting output widget context manager."""
        # TODO handle exceptions
        # if etype is not None:
        #     ip.showtraceback((etype, evalue, tb), tb_offset=0)
        self._flush()
        self.is_capturing = False
        # suppress exceptions, since they are shown above
        return True

    def _flush(self):
        """Flush stdout and stderr buffers."""
        sys.stdout.flush()
        sys.stderr.flush()

    def _append_stream_output(self, text, stream_name):
        """Append a stream output."""
        self.outputs += (
            {'output_type': 'stream', 'name': stream_name, 'text': text},
        )

    def append_stdout(self, text):
        """Append text to the stdout stream."""
        self._append_stream_output(text, stream_name='stdout')

    def append_stderr(self, text):
        """Append text to the stderr stream."""
        self._append_stream_output(text, stream_name='stderr')

    # TODO restore
    # def append_display_data(self, display_object):
    #     """Append a display object as an output.

    #     Parameters
    #     ----------
    #     display_object : IPython.core.display.DisplayObject
    #         The object to display (e.g., an instance of
    #         `IPython.display.Markdown` or `IPython.display.Image`).
    #     """
    #     fmt = InteractiveShell.instance().display_formatter.format
    #     data, metadata = fmt(display_object)
    #     self.outputs += (
    #         {
    #             'output_type': 'display_data',
    #             'data': data,
    #             'metadata': metadata
    #         },
    #     )
