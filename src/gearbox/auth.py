from . import config
import json
from authutils.token.fastapi import access_token
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)
from pcdcutils.gen3 import Gen3RequestManager, SignaturePayload
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from gearbox.errors import Forbidden, Unauthorized, NotFound
from cdislogging import get_logger

logger = get_logger("gb-auth", log_level="info")

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
security = HTTPBasic(auto_error=False)
bearer = HTTPBearer(auto_error=False)


# Authenticate incoming request
# This runs as a FastAPI dependency on protected routes
# It will validate if the request has a proper Gen3 signed signature
# If signature is missing or invalid → raise HTTP 403 (forbidden)
async def authenticate(
    request: Request, token: HTTPAuthorizationCredentials = Security(bearer)
):
    # Skip validation if BYPASS_FENCE is enabled (dev/testing mode)
    if not config.BYPASS_FENCE:

        # Read incoming request headers
        headers = dict(request.headers)

        # Get request method and path
        method_s = request.method
        path = request.url.path

        # Read request body only for POST/PUT/PATCH — otherwise leave as None
        body = None
        if method_s in ["POST", "PUT", "PATCH"]:
            body = await request.json()
        else:
            body = None

        # Initialize Gen3RequestManager — will help us check for signature
        g3rm = Gen3RequestManager(headers=headers)

        # Check if request has Gen3 signature
        if g3rm.is_gen3_signed():

            # PUBLIC_KEY is required to validate signature — check if present
            public_key = config.get("GEARBOX_MIDDLEWARE_PUBLIC_KEY")
            if not public_key:
                logger.error("No PUBLIC_KEY configured — cannot validate signature")
                raise HTTPException(
                    status_code=403,
                    detail="Missing PUBLIC_KEY — cannot validate signature",
                )

            # Prepare SignaturePayload for validation — this must match exactly what was signed
            logger.info(
                f"Signature validation starting — method: {method_s}, path: {path}"
            )
            logger.info(f"Headers: {headers}")
            logger.info(f"Body: {body}")

            payload = SignaturePayload(
                method=method_s,
                path=path,
                headers={"Gen3-Service": headers.get("Gen3-Service")},
                body=json.dumps(body, separators=(",", ":")),
            )

            # Validate the signature
            if not g3rm.valid_gen3_signature(payload, config):
                raise HTTPException(
                    status_code=403, detail="Gen3 signed request is invalid"
                )

        # If no signature is present — reject with HTTP 403
        else:
            raise HTTPException(
                status_code=403,
                detail="user does not have privileges to access this endpoint and the signature is not present.",
            )


async def authenticate_user(token: HTTPAuthorizationCredentials = Security(bearer)):
    if not config.BYPASS_FENCE:
        token_claims = await get_token_claims(token)
        user_id = token_claims.get("sub")
    else:
        user_id = config.BYPASS_FENCE_DUMMY_USER_ID
    return user_id


async def get_token_claims(token):

    try:
        issuer = None
        allowed_issuers = None

        # override token iss
        if config.FORCE_ISSUER:
            issuer = config.USER_API
            allowed_issuers = list(config.ALLOWED_ISSUERS)

        # NOTE: token can be None if no Authorization header was provided, we expect
        #       this to cause a downstream exception since it is invalid
        # access_token returns a getter function which is then called with 'token'
        token_claims = await access_token(
            "user",
            "openid",
            issuer=issuer,
            allowed_issuers=allowed_issuers,
            purpose="access",
        )(token)

    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )

    return token_claims
