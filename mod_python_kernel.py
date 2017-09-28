
from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel

from traitlets import Unicode

CODE_TEMPLATE = """
import {module}
{module}.{object}
"""


class ModPythonKernel(IPythonKernel):
    exec_module = Unicode()
    exec_object = Unicode()

    msg_types = IPythonKernel.msg_types + ['custom_message']

    def custom_message(self, stream, ident, parent):
        code = CODE_TEMPLATE.format(
            module=self.user_ns['exec_module'], 
            object=self.user_ns['exec_object']
        )
        parent['content'] = {'code': code, 'silent': False}
        super(ModPythonKernel, self).execute_request(stream, ident, parent)

    def execute_request(self, stream, ident, parent):
        pass


if __name__ == '__main__':
    import sys
    module = sys.argv[3]
    object = sys.argv[4]
    IPKernelApp.launch_instance(
        kernel_class=ModPythonKernel,
        user_ns=dict(exec_module=module, exec_object=object))