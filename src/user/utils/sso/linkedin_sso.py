from typing import Tuple

import requests

from src.config import Config
from src.user.utils.sso import BaseSSO


class LinkedinSSO(BaseSSO):
    def __init__(self):
        self.scopes = ["email", "profile", "openid"]
        self.base_auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.user_info_url = "https://api.linkedin.com/v2/userinfo"

    def get_authorization_url(self) -> str:
        return requests.get(
            url=self.base_auth_url,
            params={
                "response_type": "code",
                "client_id": Config.LINKEDIN_CLIENT_ID,
                "redirect_uri": Config.LINKEDIN_AUTH_REDIRECT_URI,
                "scope": " ".join(self.scopes),
            },
        ).url

    def get_access_token(self, code) -> str:
        response = requests.get(
            self.token_url,
            params={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": Config.LINKEDIN_AUTH_REDIRECT_URI,
                "client_id": Config.LINKEDIN_CLIENT_ID,
                "client_secret": Config.LINKEDIN_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        return response.json()["access_token"]

    def get_user_info(self, access_token) -> Tuple[str, str, str, str]:
        response = requests.get(
            self.user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = response.json()

        return (
            user_info["email"],
            user_info["given_name"],
            user_info["family_name"],
            user_info["picture"],
        )
