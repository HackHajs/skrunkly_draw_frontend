import hashlib
import secrets
import urllib.parse
from typing import NamedTuple

from auth_config import Auth0Config


class PKCEChallenge(NamedTuple):
    code_verifier: str
    code_challenge: str


def generate_pkce_challenge() -> PKCEChallenge:
    code_verifier = secrets.token_urlsafe(32)
    code_sha = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = (
        __import__("base64").urlsafe_b64encode(code_sha)
        .decode()
        .rstrip("=")
    )
    return PKCEChallenge(code_verifier, code_challenge)


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def build_authorize_url(
    config: Auth0Config,
    state: str,
    nonce: str,
    code_challenge: str,
) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "audience": config.audience,
    }
    return f"{config.authorize_url}?{urllib.parse.urlencode(params)}"
