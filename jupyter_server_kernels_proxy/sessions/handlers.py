"""Tornado handlers for the sessions web service.

Preliminary documentation at https://github.com/ipython/ipython/wiki/IPEP-16%3A-Notebook-multi-directory-dashboard-and-URL-mapping#sessions-api
"""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import asyncio
import json

import httpx

try:
    from jupyter_client.jsonutil import json_default
except ImportError:
    from jupyter_client.jsonutil import date_default as json_default

from jupyter_client.kernelspec import NoSuchKernel
from tornado import web

from jupyter_server.auth import authorized
from jupyter_server.utils import ensure_async, url_path_join

from jupyter_server.base.handlers import APIHandler

AUTH_RESOURCE = "sessions"


class SessionsAPIHandler(APIHandler):
    auth_resource = AUTH_RESOURCE


class SessionRootHandler(SessionsAPIHandler):
    @web.authenticated
    @authorized
    async def get(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/api/sessions")
        self.set_status(response.status_code)
        self.finish(response.text)

    @web.authenticated
    @authorized
    async def post(self):
        data = self.get_json_body() or {}
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.settings['proxy_url']}/api/sessions", json=data)
        self.set_status(response.status_code)
        self.finish(response.json())


class SessionHandler(SessionsAPIHandler):
    @web.authenticated
    @authorized
    async def get(self, session_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['proxy_url']}/api/sessions/{session_id}")
        self.set_status(response.status_code)
        self.finish(response.text)

    @web.authenticated
    @authorized
    async def patch(self, session_id):
        data = self.get_json_body() or {}
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{self.settings['proxy_url']}/api/sessions/{session_id}", json=data)
        self.set_status(response.status_code)
        self.finish(response.json())

    @web.authenticated
    @authorized
    async def delete(self, session_id):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.settings['proxy_url']}/api/sessions/{session_id}")
        self.set_status(response.status_code)
        self.finish(response.json())


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------

_session_id_regex = r"(?P<session_id>\w+-\w+-\w+-\w+-\w+)"

default_handlers = [
    (r"/api/sessions/%s" % _session_id_regex, SessionHandler),
    (r"/api/sessions", SessionRootHandler),
]
