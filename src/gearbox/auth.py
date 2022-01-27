from . import config, logger
from authutils.token.fastapi import access_token
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from . import config
from starlette.status import (
    HTTP_401_UNAUTHORIZED
)

def authenticate_user():
    # auto_error=False prevents FastAPI from raises a 403 when the request is missing
    # an Authorization header. Instead, we want to return a 401 to signify that we did
    # not recieve valid credentials
    bearer = HTTPBearer(auto_error=False)

    token = Security(bearer)
    if not config.BYPASS_FENCE:
        token_claims = get_token_claims(token)
        user_id = token_claims.get("sub")
    else:
        user_id = 4

    return user_id

def get_token_claims(token):

    try:
        issuer = None
        allowed_issuers = None

        # override token iss 
        if config.FORCE_ISSUER:
            issuer = config.USER_API
            allowed_issuers =  list(config.ALLOWED_ISSUERS)

        # NOTE: token can be None if no Authorization header was provided, we expect
        #       this to cause a downstream exception since it is invalid
        token_claims = access_token("user", "openid", issuer=issuer, allowed_issuers=allowed_issuers, purpose="access")(token)

    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )

    return token_claims
