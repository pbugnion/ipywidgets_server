from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel


code = """
from ipywidgets import IntSlider, Text, VBox
s = IntSlider(max=200, value=100)
t = Text()

def update_text(change=None):
    t.value = str(float(s.value) ** 2)

s.observe(update_text, names='value')
update_text()
VBox([s, t])
"""


class ModPythonKernel(IPythonKernel):

    msg_types = IPythonKernel.msg_types + ['custom_message']

    def custom_message(self, stream, ident, parent):
        parent['content'] = {'code': code, 'silent': False}
        super(ModPythonKernel, self).execute_request(stream, ident, parent)

    def execute_request(self, stream, ident, parent):
        raise NotImplementedError()


if __name__ == '__main__':
    IPKernelApp.launch_instance(kernel_class=ModPythonKernel)