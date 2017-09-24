
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
    pass

    def find_kernel_specs(self):
        return {'mod_python': root}


ksm = CustomKernelSpecManager()


class CustomKernelManager(MappingKernelManager):

    @property
    def default_kernel_name(self):
        return 'mod_python'

    @property
    def kernel_spec_manager(self):
        return ksm

    # @gen.coroutine
    # def start_kernel(self, *args, **kwargs):
    #     print('starting kernel...')
    #     kernel_id = yield gen.maybe_future(super(CustomKernelManager, self).start_kernel(*args, **kwargs))
    #     if kernel_id:
    #         kernel = self.get_kernel(kernel_id)
    #         client = kernel.client()
    #         client.start_channels()
    #         client.wait_for_ready()
    #         client.execute('a = 53')
    #         msg = client.shell_channel.get_msg(block=True)
    #         print(msg)
    #         msg = client.iopub_channel.get_msg(block=True)
    #         print(msg)
    #         client.stop_channels()
    #     raise gen.Return(kernel_id)


m = CustomKernelManager()


class CustomKernelHandler(MainKernelHandler):
    @property
    def kernel_manager(self):
        return m


class CustomChannelHandler(ZMQChannelsHandler):
    @property
    def kernel_manager(self):
        return m


class CustomKernelSpecHandler(MainKernelSpecHandler):
    @property
    def kernel_manager(self):
        return m

    @property
    def kernel_spec_manager(self):
        return ksm

    # @json_errors
    # def get(self):
    #     model = {}

    #     self.set_header("Content-Type", 'application/json')
    #     self.finish(json.dumps(model))



_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"
_kernel_action_regex = r"(?P<action>restart|interrupt)"


def make_app():
    return tornado.web.Application([
        (r'/api/kernels', CustomKernelHandler),
        (r'/api/kernels/%s/channels' % _kernel_id_regex, CustomChannelHandler),
        (r'/api/kernelspecs', CustomKernelSpecHandler),
        (
            r"/(.*)", 
            tornado.web.StaticFileHandler, 
            {
                'path': root,
                'default_filename': 'index.html'
            }
        ),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()