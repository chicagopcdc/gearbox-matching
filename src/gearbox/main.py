import asyncio
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
import click
from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic import ValidationError
import httpx
from sqlalchemy.orm import Session
from sqlalchemy import text
from gearbox import deps, config
from gearboxdatamodel.util import status
import cdislogging
from pcdc_aws_client.boto import BotoManager
from pcdcutils.signature import SignatureManager
from pcdcutils.errors import KeyPathInvalidError, NoKeyError


logger_name = "gb-logger"
logger = cdislogging.get_logger(
    logger_name, log_level="debug" if config.DEBUG else "info"
)


from importlib_metadata import entry_points, version


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up application")
    
    # Test database connection
    logger.info("Testing database connection...")
    try:
        from gearbox.util.db import engine
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.scalar()
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    
    app.include_router(router)
    load_modules(app)
    
    @app.exception_handler(ResponseValidationError)
    async def validation_exception_handler(request: Request, exc: ValueError):
        exc_str = f"{exc}.".replace("\n", "").replace(" ", " ")
        logger.error(f"PYDANTIC RESPONSE VALIDATION ERROR: {request.url}: {exc_str}")
        content = {"status_code": 10422, "message": exc_str, "data": None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: ValueError):
        exc_str = f"{exc}.".replace("\n", "").replace(" ", " ")
        logger.error(f"PYDANTIC REQUEST VALIDATION ERROR: {request.url}: {exc_str}")
        content = {"status_code": 10422, "message": exc_str, "data": None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValueError):
        exc_str = f"{exc}.".replace("\n", "").replace(" ", " ")
        logger.error(f"PYDANTIC VALIDATION ERROR: {request.url}: {exc_str}")
        content = {
            "status_code": 10422,
            "message": "PYDANTIC ValidationError" + exc_str,
            "data": None,
        }
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    app.async_client = httpx.AsyncClient()
    app.boto_manager = BotoManager(
        {
            "region_name": config.AWS_REGION,
            "aws_access_key_id": config.S3_AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": config.S3_AWS_SECRET_ACCESS_KEY,
        },
        logger,
    )
    load_keys()
    logger.info("Application startup complete")

    yield

    # Shutdown logic
    logger.info("Clearing sensitive configuration data...")
    config.S3_AWS_ACCESS_KEY_ID = None
    config.S3_AWS_SECRET_ACCESS_KEY = None
    config.DB_PASSWORD = None
    config.DB_STRING = None
    config.ALEMBIC_DB_STRING = None
    config.ADMIN_LOGINS = []
    config.DB_DSN = None
    logger.info("Closing async client.")
    await app.async_client.aclose()
    logger.info("Disposing database engine.")
    from gearbox.util.db import engine
    await engine.dispose()
    logger.info("Dispose of aws client.")
    app.boto_manager = None
    logger.info("Application shutdown complete")


def get_app():
    app = FastAPI(
        title="Framework Services Object Management Service",
        version=pkg_resources.get_distribution("gearbox").version,
        debug=config.DEBUG,
        openapi_prefix=config.URL_PREFIX,
        lifespan=lifespan,
    )
    app.add_middleware(ClientDisconnectMiddleware)
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
    for ep in entry_points().select(group="gearbox.modules"):
        mod = ep.load()
        if app and hasattr(mod, "init_app"):
            mod.init_app(app)
        msg = "Loaded module: "
        logger.info(
            msg + "%s",
            ep.name,
            extra={"color_message": msg + click.style("%s", fg="cyan")},
        )


def load_keys():
    try:
        config.GEARBOX_KEY_CONFIG["GEARBOX_MIDDLEWARE_PUBLIC_KEY"] = SignatureManager(
            key_path=config.GEARBOX_MIDDLEWARE_PUBLIC_KEY_Path
        ).key
    except NoKeyError:
        logger.warning("GEARBOX_PUBLIC_KEY not found")
    except KeyPathInvalidError:
        logger.warning("GEARBOX_PUBLIC_KEY_PATH invalid")


router = APIRouter()


@router.get("/version")
def get_version():
    return version("gearbox")


@router.get("/_status")
async def get_status(db: Session = Depends(deps.get_session)):
    now = await db.execute(text("SELECT now()"))
    return dict(status="OK", timestamp=now.scalars().first())
