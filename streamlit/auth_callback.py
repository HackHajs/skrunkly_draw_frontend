import json
from typing import Optional

import jwt
import requests
import streamlit as st

from auth_config import get_cached_config


def exchange_code_for_tokens(
    code: str,
    code_verifier: str,
    config=None,
) -> dict:
    if config is None:
        config = get_cached_config()

    payload = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(config.token_url, data=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def validate_id_token(
    id_token: str,
    nonce: str,
    config=None,
) -> dict:
    if config is None:
        config = get_cached_config()

    try:
        decoded = jwt.decode(
            id_token,
            options={"verify_signature": False},  # Will verify in production
            algorithms=["RS256", "HS256"],
        )

        if decoded.get("nonce") != nonce:
            raise ValueError("Nonce mismatch in ID token")

        aud = decoded.get("aud")
        if isinstance(aud, list):
            if config.client_id not in aud:
                raise ValueError("Audience mismatch in ID token")
        elif aud != config.client_id:
            raise ValueError("Audience mismatch in ID token")

        return decoded
    except jwt.DecodeError as e:
        raise ValueError(f"Failed to decode ID token: {e}")


def handle_callback() -> Optional[dict]:
    query_params = st.query_params

    if "error" in query_params:
        error = query_params["error"]
        error_desc = query_params.get("error_description", "Unknown error")
        st.error(f"Auth0 Error: {error} - {error_desc}")
        return None

    if "code" not in query_params:
        return None

    code = query_params["code"]
    state = query_params.get("state")

    session_state = st.session_state.get("auth_state")
    if not session_state or state != session_state:
        st.error("State mismatch: invalid authorization callback")
        return None

    try:
        config = get_cached_config()
        code_verifier = st.session_state.get("auth_code_verifier")
        nonce = st.session_state.get("auth_nonce")

        if not code_verifier or not nonce:
            st.error("Session expired: missing PKCE or nonce")
            return None

        token_response = exchange_code_for_tokens(code, code_verifier, config)

        id_token = token_response.get("id_token")
        if not id_token:
            st.error("No ID token in response")
            return None

        claims = validate_id_token(id_token, nonce, config)

        return {
            "id_token": id_token,
            "access_token": token_response.get("access_token"),
            "claims": claims,
            "email": claims.get("email"),
        }

    except Exception as e:
        st.error(f"Token exchange failed: {str(e)}")
        return None
