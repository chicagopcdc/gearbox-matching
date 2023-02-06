import asyncio
import json
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse
# from pydantic import ValidationError
# from jsonschema import ValidationError
import click
import pkg_resources
from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request
from fastapi.exceptions import RequestValidationError
import httpx
from sqlalchemy.orm import Session
from gearbox import deps, config
from gearbox.util import status
import cdislogging
from pcdc_aws_client.boto import BotoManager

logger_name = 'gb-logger'
logger = cdislogging.get_logger(logger_name, log_level="debug" if config.DEBUG else "info")



#try:
    # importlib.metadata works locally but not in Docker
    # trying importlib_metadata
    # from importlib.metadata import entry_points
from importlib_metadata import entry_points
#except ImportError:
#    from importlib_metadata import entry_points

def get_app():
    app = FastAPI(
        title="Framework Services Object Management Service",
        version=pkg_resources.get_distribution("gearbox").version,
        debug=config.DEBUG,
        openapi_prefix=config.URL_PREFIX,
    )
    app.include_router(router)
    app.add_middleware(ClientDisconnectMiddleware)
    load_modules(app)
    app.async_client = httpx.AsyncClient()

    app.boto_manager = BotoManager(
        {
            'region_name': config.AWS_REGION,
            'aws_access_key_id': config.S3_AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': config.S3_AWS_SECRET_ACCESS_KEY
        }, 
        logger)

    @app.exception_handler(RequestValidationError)
    async def value_error_exception_handler(request:Request, exc:ValueError):
        return PlainTextResponse(str(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Closing async client.")
        await app.async_client.aclose()

    return app


class ClientDisconnectMiddleware:
    def __init__(self, app):
        self._app = app

    async def __call__(self, scope, receive, send):
        loop = asyncio.get_running_loop()
        rv = loop.create_task(self._app(scope, receive, send))
        waiter = None
        cancelled = False
        if scope["type"] == "http":

            def add_close_watcher():
                nonlocal waiter

                async def wait_closed():
                    nonlocal cancelled
                    while True:
                        message = await receive()
                        if message["type"] == "http.disconnect":
                            if not rv.done():
                                cancelled = True
                                rv.cancel()
                            break

                waiter = loop.create_task(wait_closed())

            scope["add_close_watcher"] = add_close_watcher
        try:
            await rv
        except asyncio.CancelledError:
            if not cancelled:
                raise
        if waiter and not waiter.done():
            waiter.cancel()


def load_modules(app=None):
    logger.info("Start to load modules.")
    for ep in entry_points()["gearbox.modules"]:
        mod = ep.load()
        if app and hasattr(mod, "init_app"):
            mod.init_app(app)
        msg = "Loaded module: "
        logger.info(
            msg + "%s",
            ep.name,
            extra={"color_message": msg + click.style("%s", fg="cyan")},
        )


router = APIRouter()


@router.get("/version")
def get_version():
    return pkg_resources.get_distribution("gearbox").version


@router.get("/_status")
async def get_status(db: Session = Depends(deps.get_session)):
    now = await db.execute("SELECT now()")
    return dict( status="OK", timestamp=now.scalars().first())
