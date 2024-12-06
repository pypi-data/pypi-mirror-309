import pathlib
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp
from fast_license.license import LicenseDecorator


class LicenseMiddleware(BaseHTTPMiddleware):
    license_model: LicenseDecorator
    def __init__(self, app: ASGIApp, license_path: pathlib.Path, private_key: str) -> None: ...
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response: ...
