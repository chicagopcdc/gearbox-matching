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
from . import config
from pcdcutils.gen3 import Gen3RequestManager
from pcdcutils.signature import SignatureManager
from starlette.status import (
    HTTP_401_UNAUTHORIZED
)
from cdislogging import get_logger
logger = get_logger('gb-auth', log_level='info')

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
security = HTTPBasic(auto_error=False)
bearer = HTTPBearer(auto_error=False)

async def authenticate(
    request: Request,
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    if not config.BYPASS_FENCE:
        g3rm = Gen3RequestManager(headers=request.headers)
        if g3rm.is_gen3_signed():
            if request.headers['gen3-service'] == 'gearbox_middleware' and 'GEARBOX_MIDDLEWARE_PUBLIC_KEY' not in config.GEARBOX_KEY_CONFIG:
                logger.error("no public key found")
                raise HTTPException(HTTP_401_UNAUTHORIZED, "missing public key")
            else:
                data = await request.json()
                if not g3rm.valid_gen3_signature(json.dumps(data), config=config.GEARBOX_KEY_CONFIG):
                    raise HTTPException(HTTP_401_UNAUTHORIZED, "Gen3 signed request is invalid")
        else:
            token_claims = await get_token_claims(token)

async def authenticate_user(
    token: HTTPAuthorizationCredentials = Security(bearer)
):
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
            allowed_issuers =  list(config.ALLOWED_ISSUERS)

        # NOTE: token can be None if no Authorization header was provided, we expect
        #       this to cause a downstream exception since it is invalid
        # access_token returns a getter function which is then called with 'token'
        token_claims = await access_token("user", "openid", issuer=issuer, allowed_issuers=allowed_issuers, purpose="access")(token)

    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )

    return token_claims
