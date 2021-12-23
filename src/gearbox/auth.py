from . import config, logger
from authutils.token.fastapi import access_token
from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED
)

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
        token_claims = await access_token("user", "openid", issuer=issuer, allowed_issuers=allowed_issuers, purpose="access")(token)

    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )

    return token_claims
