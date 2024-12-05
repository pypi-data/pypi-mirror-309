import typing
from httpx import Auth, Request, Response


class BearerAuth(Auth):
    def __init__(self, token: str):
        self._auth_header = self._build_auth_header(token)

    def _build_auth_header(self, token: str) -> str:
        return f"bearer {token}"

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers["Authorization"] = self._auth_header
        yield request
