
import logging
import sys

from ipykernel.kernelapp import IPKernelApp

from . import WidgetsServerKernel

module = sys.argv[3]
object = sys.argv[4]
IPKernelApp.launch_instance(
    kernel_class=WidgetsServerKernel,
    log_level=logging.DEBUG,
    user_ns=dict(exec_module=module, exec_object=object))