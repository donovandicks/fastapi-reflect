import logfire
from fastapi import FastAPI

from fastapi_reflect.services.docs import DocsService
from fastapi_reflect.transport import register_routers

logfire.configure()

app = FastAPI(
    root_path="/api",
    servers=[{"url": "http://127.0.0.1:8000/api"}],
    root_path_in_servers=False,
)
_ = DocsService(app)

logfire.instrument_pydantic()
logfire.instrument_fastapi(app)

register_routers(app)
