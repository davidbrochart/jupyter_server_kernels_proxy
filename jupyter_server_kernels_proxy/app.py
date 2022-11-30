from jupyter_server.extension.application import ExtensionApp
from jupyter_server_kernels.kernels.kernelmanager import MappingKernelManager
from traitlets import Unicode

from .kernels import handlers, websocket
from .sessions import handlers


class KernelsProxyExtensionApp(ExtensionApp):

    name = "jupyter_server_kernels_proxy"

    proxy_url = Unicode(
        help="The URL from where to proxy kernels."
    ).tag(config=True)

    def initialize_settings(self):
        self.settings.update(dict(
            kernels_available=True,
            proxy_url=self.proxy_url,
            kernel_manager=KernelManager()
        ))

    def initialize_handlers(self):
        self.handlers.extend(websocket.default_handlers)
        self.handlers.extend(handlers.default_handlers)
        self.serverapp.web_app.settings["kernels_available"] = self.settings[
            "kernels_available"
        ]

class KernelManager(MappingKernelManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
