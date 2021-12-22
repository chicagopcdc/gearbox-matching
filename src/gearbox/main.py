import asyncio
import click
import pkg_resources
from fastapi import FastAPI, APIRouter, HTTPException, Depends
import httpx
from sqlalchemy.orm import Session
from . import logger, config
from gearbox import deps

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points



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

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Closing async client.")
        await app.async_client.aclose()

    # @app.on_event("startup")
    # async def startup_event():
    #     logger.info("Do something at startup")
    #     await {blank}.init(
    #         hostname=url_parts.hostname, port=url_parts.port
    #     )

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
# async def get_status(db: Session = Depends(deps.get_db)):
async def get_status(db: Session = Depends(deps.get_session)):
    try:
        now = await db.execute("SELECT now()")
        return dict( status="OK", timestamp=now.scalars().first())
    except Exception:
        raise UnhealthyCheck("Unhealthy")
