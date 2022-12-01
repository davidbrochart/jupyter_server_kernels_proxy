from pathlib import Path
from tempfile import TemporaryDirectory

import httpx
from tornado import web
from jupyter_server.auth import authorized
from jupyter_server.base.handlers import APIHandler, JupyterHandler


AUTH_RESOURCE = "kernelspecs"


class KernelSpecsAPIHandler(APIHandler):
    auth_resource = AUTH_RESOURCE


class MainKernelSpecHandler(KernelSpecsAPIHandler):
    @web.authenticated
    @authorized
    async def get(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/api/kernelspecs")
        self.set_status(response.status_code)
        self.finish(response.text)


class KernelSpecHandler(KernelSpecsAPIHandler):
    @web.authenticated
    @authorized
    async def get(self, kernel_name):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/api/kernelspecs/{kernel_name}")
        self.set_status(response.status_code)
        self.finish(response.text)

class KernelSpecResourceHandler(web.StaticFileHandler, JupyterHandler):
    SUPPORTED_METHODS = ("GET", "HEAD")
    auth_resource = AUTH_RESOURCE
    temporary_directory = Path(TemporaryDirectory(prefix='jupyter_server_kernels_proxy_').name)

    def initialize(self):
        web.StaticFileHandler.initialize(self, path="")

    @web.authenticated
    @authorized
    async def get(self, kernel_name, path, include_body=True):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/kernelspecs/{kernel_name}/{path}")

        p = self.temporary_directory / kernel_name / path
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(response.content)
        if path.lower().endswith(".png"):
            self.set_header("Cache-Control", f"max-age={60*60*24*30}")
        self.root = p.parent
        return await web.StaticFileHandler.get(self, p, include_body=include_body)

    @web.authenticated
    @authorized
    async def head(self, kernel_name, path):
        return await self.get(kernel_name, path, include_body=False)


kernel_name_regex = r"(?P<kernel_name>[\w\.\-%]+)"

default_handlers = [
    (r"/api/kernelspecs", MainKernelSpecHandler),
    (r"/api/kernelspecs/%s" % kernel_name_regex, KernelSpecHandler),
    (r"/kernelspecs/%s/(?P<path>.*)" % kernel_name_regex, KernelSpecResourceHandler),
]
