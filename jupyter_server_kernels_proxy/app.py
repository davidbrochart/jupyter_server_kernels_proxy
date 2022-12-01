from jupyter_server.extension.application import ExtensionApp
from traitlets import Unicode

from .kernels import handlers as kernels_handlers, websocket
from .kernelspecs import handlers as kernelspecs_handlers
from .sessions import handlers as sessions_handlers


class KernelsProxyExtensionApp(ExtensionApp):

    name = "jupyter_server_kernels_proxy"

    proxy_url = Unicode(
        help="The URL from where to proxy kernels."
    ).tag(config=True)

    def initialize_settings(self):
        self.settings.update(dict(
            kernels_available=True,
            proxy_url=self.proxy_url,
        ))

    def initialize_handlers(self):
        self.handlers.extend(websocket.default_handlers)
        self.handlers.extend(kernels_handlers.default_handlers)
        self.handlers.extend(kernelspecs_handlers.default_handlers)
        self.handlers.extend(sessions_handlers.default_handlers)
        self.serverapp.web_app.settings["kernels_available"] = self.settings[
            "kernels_available"
        ]
