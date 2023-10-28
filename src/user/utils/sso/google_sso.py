from typing import Tuple

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from src.config import Config
from src.user.utils.sso import BaseSSO


class GoogleSSO(BaseSSO):
    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]
        self.credentials = {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "project_id": Config.GOOGLE_PROJECT_ID,
            "auth_uri": Config.GOOGLE_AUTH_URI,
            "token_uri": Config.GOOGLE_TOKEN_URI,
            "auth_provider_x509_cert_url": Config.GOOGLE_AUTH_PROVIDER_X509_CERT_URL,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
        }
        self.flow = Flow.from_client_config(
            client_config={"web": self.credentials},
            scopes=self.scopes,
            redirect_uri=Config.GOOGLE_AUTH_REDIRECT_URI,
        )

    def get_authorization_url(self) -> str:
        auth_url, state = self.flow.authorization_url()
        return auth_url

    def get_access_token(self, code) -> str:
        self.flow.fetch_token(code=code)
        return self.flow.credentials

    def get_user_info(self, credentials: Credentials) -> Tuple[str, str, str, str]:
        service = build("oauth2", "v2", credentials=credentials)
        user_info = service.userinfo().get().execute()
        return (
            user_info["email"],
            user_info["given_name"],
            user_info["family_name"],
            user_info["picture"],
        )
