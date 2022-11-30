import json
from pathlib import Path
from typing import Optional

import httpx
from tornado import web

from jupyter_server.auth.decorator import authorized
from jupyter_server.base.handlers import APIHandler


AUTH_RESOURCE = "kernels"


class KernelsAPIHandler(APIHandler):
    auth_resource = AUTH_RESOURCE


class MainKernelHandler(KernelsAPIHandler):
    @web.authenticated
    @authorized
    async def get(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/api/kernels")
        self.set_status(response.status_code)
        self.finish(response.text)

    @web.authenticated
    @authorized
    async def post(self):
        data = self.get_json_body() or {}
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.settings['proxy_url']}/api/kernels", data=data)
        self.set_status(response.status_code)
        self.finish(response.json())

class KernelHandler(KernelsAPIHandler):
    @web.authenticated
    @authorized
    async def get(self, kernel_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/api/kernels/{kernel_id}")
        self.set_status(response.status_code)
        self.finish(response.text)

    @web.authenticated
    @authorized
    async def delete(self, kernel_id):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.settings['proxy_url']}/api/kernels/{kernel_id}")
        self.set_status(response.status_code)
        self.finish(response.json())

class KernelActionHandler(KernelsAPIHandler):
    @web.authenticated
    @authorized
    async def post(self, kernel_id, action):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.settings['proxy_url']}/api/kernels/{kernel_id}/{action}")
        self.set_status(response.status_code)
        self.finish(response.json())

_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"
_kernel_action_regex = r"(?P<action>restart|interrupt)"

default_handlers = [
    (r"/api/kernels", MainKernelHandler),
    (r"/api/kernels/%s" % _kernel_id_regex, KernelHandler),
    (
        rf"/api/kernels/{_kernel_id_regex}/{_kernel_action_regex}",
        KernelActionHandler,
    ),
]
