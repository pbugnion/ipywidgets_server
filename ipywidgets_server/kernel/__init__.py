
import logging

from ipykernel.kernelbase import Kernel
from ipykernel.ipkernel import IPythonKernel

from traitlets import Unicode

CODE_TEMPLATE = """
import {module}
{module}.{object}
"""


class WidgetsServerKernel(IPythonKernel):
    exec_module = Unicode()
    exec_object = Unicode()

    msg_types = IPythonKernel.msg_types + ['custom_message']

    def custom_message(self, stream, ident, parent):
        code = CODE_TEMPLATE.format(
            module=self.user_ns['exec_module'], 
            object=self.user_ns['exec_object']
        )
        parent['content'] = {'code': code, 'silent': False}
        super(WidgetsServerKernel, self).execute_request(stream, ident, parent)

    def execute_request(self, stream, ident, parent):
        pass