
from zmq.eventloop import ioloop
ioloop.install()

import os
import json

import tornado.ioloop
import tornado.web
from tornado import gen

from notebook.services.kernels.handlers import MainKernelHandler, ZMQChannelsHandler
from notebook.services.kernels.kernelmanager import MappingKernelManager
from notebook.services.kernelspecs.handlers import MainKernelSpecHandler
from notebook.base.handlers import json_errors
from jupyter_client.kernelspec import KernelSpecManager


root = os.path.dirname(__file__)

class CustomKernelSpecManager(KernelSpecManager):

    def find_kernel_specs(self):
        return {'mod_python': root}


ksm = CustomKernelSpecManager()

m = MappingKernelManager(
    default_kernel_name='mod_python', 
    kernel_spec_manager=ksm
)


_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"
_kernel_action_regex = r"(?P<action>restart|interrupt)"


def make_app():
    return tornado.web.Application(
        [
            (r'/api/kernels', MainKernelHandler),
            (r'/api/kernels/%s/channels' % _kernel_id_regex, ZMQChannelsHandler),
            (r'/api/kernelspecs', MainKernelSpecHandler),
            (
                r"/(.*)", 
                tornado.web.StaticFileHandler, 
                {
                    'path': root,
                    'default_filename': 'index.html'
                }
            )
        ],
        kernel_manager=m,
        kernel_spec_manager=ksm
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()