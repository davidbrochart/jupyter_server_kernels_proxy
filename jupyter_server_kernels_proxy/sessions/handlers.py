import httpx

from tornado import web

from jupyter_server.auth import authorized

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
