from typing import Any

from fastapi import FastAPI

from fastapi_reflect.utils import SingletonMeta


class DocsService(metaclass=SingletonMeta):
    app: FastAPI

    def __new__(cls, app: FastAPI) -> None:
        cls.app = app

    @classmethod
    def get_spec(cls) -> dict[str, Any]:
        return cls.app.openapi()
