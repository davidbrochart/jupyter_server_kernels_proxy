import asyncio

from tornado.websocket import WebSocketHandler
from tornado import web
from websockets import connect

from jupyter_server.auth.utils import warn_disabled_authorization
from jupyter_server.base.handlers import JupyterHandler

from .handlers import _kernel_id_regex


AUTH_RESOURCE = "kernels"


class KernelWebsocketHandler(WebSocketHandler, JupyterHandler):

    auth_resource = AUTH_RESOURCE

    def get(self, kernel_id):
        user = self.current_user

        if not user:
            raise web.HTTPError(403)

        # authorize the user.
        if not self.authorizer:
            # Warn if an authorizer is unavailable.
            warn_disabled_authorization()
        elif not self.authorizer.is_authorized(self, user, "execute", self.auth_resource):
            raise web.HTTPError(403)

        self.kernel_id = kernel_id
        self.session_id = self.get_argument("session_id", None)
        return super().get(kernel_id=kernel_id)

    async def open(self, kernel_id):
        proxy_url = self.settings['proxy_url']
        ws_url = "ws" + proxy_url[proxy_url.find(":"):]
        self.websocket = await connect(f"{ws_url}/api/kernels/{self.kernel_id}/channels?session_id={self.session_id}")
        asyncio.create_task(self.process_messages())

    async def on_message(self, message):
        """Get a kernel message from the websocket and turn it into a ZMQ message."""
        await self.websocket.send(message)

    async def process_messages(self):
        while True:
            try:
                message = await self.websocket.recv()
                self.write_message(message, binary=False)
            except Exception:
                break

    def on_close(self):
        #asyncio.create_task(self.websocket.close())
        #self.websocket = None
        pass

default_handlers = [
    (r"/api/kernels/%s/channels" % _kernel_id_regex, KernelWebsocketHandler),
]
