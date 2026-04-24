import os
from dataclasses import dataclass

import streamlit as st
from dotenv import load_dotenv


@dataclass
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str
    audience: str
    redirect_uri: str

    @property
    def authorize_url(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"


def load_config() -> Auth0Config:
    load_dotenv()

    def get_secret(key: str, env_key: str = None) -> str:
        env_key = env_key or key.upper()
        try:
            return st.secrets[key]
        except (FileNotFoundError, KeyError):
            value = os.getenv(env_key)
            if value is None:
                raise ValueError(
                    f"Missing Auth0 configuration: {key}. "
                    f"Set it in .streamlit/secrets.toml or .env file as {env_key}."
                )
            return value

    return Auth0Config(
        domain=get_secret("auth0_domain"),
        client_id=get_secret("auth0_client_id"),
        client_secret=get_secret("auth0_client_secret"),
        audience=get_secret("auth0_audience"),
        redirect_uri=get_secret("auth0_redirect_uri"),
    )


@st.cache_resource
def get_cached_config() -> Auth0Config:
    return load_config()
