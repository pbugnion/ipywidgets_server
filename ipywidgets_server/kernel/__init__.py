
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

    # Restrict the message types to disallow arbitrary code execution
    msg_types = ['comm_info_request', 'kernel_info_request', 'custom_message', 'shutdown_request']

    def custom_message(self, stream, ident, parent):
        code = CODE_TEMPLATE.format(
            module=self.user_ns['exec_module'], 
            object=self.user_ns['exec_object']
        )
        parent['content'] = {'code': code, 'silent': False}
        super(WidgetsServerKernel, self).execute_request(stream, ident, parent)