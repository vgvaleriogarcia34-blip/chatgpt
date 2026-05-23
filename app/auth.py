import msal
from . import config


def _build_msal_app(cache: msal.SerializableTokenCache | None = None) -> msal.ConfidentialClientApplication:
    return msal.ConfidentialClientApplication(
        client_id=config.MS_CLIENT_ID,
        client_credential=config.MS_CLIENT_SECRET,
        authority=config.MS_AUTHORITY,
        token_cache=cache,
    )


def build_auth_url(state: str) -> str:
    app = _build_msal_app()
    return app.get_authorization_request_url(
        scopes=config.MS_SCOPES,
        state=state,
        redirect_uri=config.MS_REDIRECT_URI,
    )


def exchange_code(code: str) -> dict:
    cache = msal.SerializableTokenCache()
    app = _build_msal_app(cache=cache)
    result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=config.MS_SCOPES,
        redirect_uri=config.MS_REDIRECT_URI,
    )
    if "error" in result:
        raise RuntimeError(f"{result.get('error')}: {result.get('error_description')}")
    return {"token": result, "cache": cache.serialize()}


def acquire_token_silent(cache_str: str) -> tuple[str | None, str]:
    cache = msal.SerializableTokenCache()
    if cache_str:
        cache.deserialize(cache_str)
    app = _build_msal_app(cache=cache)
    accounts = app.get_accounts()
    if not accounts:
        return None, cache.serialize()
    result = app.acquire_token_silent(config.MS_SCOPES, account=accounts[0])
    if not result or "access_token" not in result:
        return None, cache.serialize()
    return result["access_token"], cache.serialize()
