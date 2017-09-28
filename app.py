
from zmq.eventloop import ioloop

ioloop.install()  # This needs to happen before the tornado imports

import os  # noqa: E402
import shutil  # noqa: E402
import tempfile  # noqa: E402
import json

import tornado.ioloop  # noqa: E402
import tornado.web  # noqa: E402

from notebook.services.kernels.handlers import (  # noqa: E402
    MainKernelHandler, ZMQChannelsHandler
)

from notebook.utils import url_path_join, url_escape

from notebook.services.kernels.kernelmanager \
    import MappingKernelManager  # noqa: E402
from notebook.services.kernelspecs.handlers \
    import MainKernelSpecHandler  # noqa: E402
from jupyter_client.kernelspec \
    import KernelSpecManager  # noqa: E402

from jupyter_client.jsonutil import date_default


ROOT = os.path.dirname(__file__)
CODE = 'test'
OBJECT = 'vbox'


class CustomKernelSpecManager(KernelSpecManager):

    def find_kernel_specs(self):
        return {'mod_python': ROOT}


class CustomKernelHandler(MainKernelHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        km = self.kernel_manager
        model = self.get_json_body()
        if model is None:
            model = {
                'name': km.default_kernel_name
            }
        else:
            model.setdefault('name', km.default_kernel_name)

        kernel_id = yield tornado.gen.maybe_future(km.start_kernel(kernel_name=model['name'], extra_arguments=[CODE, OBJECT]))
        model = km.kernel_model(kernel_id)
        location = url_path_join(self.base_url, 'api', 'kernels', url_escape(kernel_id))
        self.set_header('Location', location)
        self.set_status(201)
        self.finish(json.dumps(model, default=date_default))


_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"


def make_app(connection_dir):
    kernel_spec_manager = CustomKernelSpecManager()
    kernel_manager = MappingKernelManager(
        default_kernel_name='mod_python',
        kernel_spec_manager=kernel_spec_manager,
        connection_dir=connection_dir
    )
    handlers = [
        (r'/api/kernels', CustomKernelHandler),
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
    ]
    return tornado.web.Application(
        handlers,
        kernel_manager=kernel_manager,
        kernel_spec_manager=kernel_spec_manager
    )


if __name__ == "__main__":
    connection_dir = tempfile.mkdtemp()
    print(f'Using {connection_dir} to store connection files')
    try:
        app = make_app(connection_dir)
        app.listen(8889)
        tornado.ioloop.IOLoop.current().start()
    finally:
        shutil.rmtree(connection_dir)
