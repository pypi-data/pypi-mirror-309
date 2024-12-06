import pathlib
from pydantic import BaseModel
from fastapi import APIRouter

class BaseResponse(BaseModel):
    code: int
    msg: str

class LicenseModel(BaseModel):
    value: str

class APILicense:
    router: APIRouter
    _router: APIRouter
    license_path: pathlib.Path
    def __init__(self, license_path: pathlib.Path, private_key: str) -> None: ...
    def register(self, hosts: list[str], port: int) -> None: ...
