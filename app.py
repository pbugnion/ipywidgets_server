
from zmq.eventloop import ioloop

ioloop.install()  # This needs to happen before the tornado imports

import os  # noqa: E402

import tornado.ioloop  # noqa: E402
import tornado.web  # noqa: E402

from notebook.services.kernels.handlers import (  # noqa: E402
    MainKernelHandler, ZMQChannelsHandler
)
from notebook.services.kernels.kernelmanager \
    import MappingKernelManager  # noqa: E402
from notebook.services.kernelspecs.handlers \
    import MainKernelSpecHandler  # noqa: E402
from jupyter_client.kernelspec \
    import KernelSpecManager  # noqa: E402


ROOT = os.path.dirname(__file__)


class CustomKernelSpecManager(KernelSpecManager):

    def find_kernel_specs(self):
        return {'mod_python': ROOT}


_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"


def make_app():
    kernel_spec_manager = CustomKernelSpecManager()
    kernel_manager = MappingKernelManager(
        default_kernel_name='mod_python', 
        kernel_spec_manager=kernel_spec_manager
    )
    return tornado.web.Application(
        [
            (r'/api/kernels', MainKernelHandler),
            (r'/api/kernels/%s/channels' % _kernel_id_regex, ZMQChannelsHandler),
            (r'/api/kernelspecs', MainKernelSpecHandler),
            (
                r"/(.*)", 
                tornado.web.StaticFileHandler, 
                {
                    'path': ROOT,
                    'default_filename': 'index.html'
                }
            )
        ],
        kernel_manager=kernel_manager,
        kernel_spec_manager=kernel_spec_manager
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()